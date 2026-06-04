// In-process concurrency queue for fuzz dispatch.
//
// The bot may receive several fuzz requests in a short window (e.g. a PR author
// pushes three times in a row, or a batch of repository_dispatch events lands).
// We must not run an unbounded number of containers at once, and we should not
// waste a slot fuzzing a head_sha that a newer push has already obsoleted.
//
// Semantics
// ---------
//   * Concurrency: at most FUZZ_MAX_CONCURRENCY tasks run their callback
//     simultaneously (env-read at construction, clamped to >= 1, default 1).
//   * Keyed supersede: callers pass a `key` (e.g. "owner/repo#<pr>"). At most one
//     task per key is ever *waiting*. If a new task arrives for a key whose prior
//     task has NOT started yet, the prior task is *superseded*: it never runs and
//     its promise rejects with `SupersededError`. The newest enqueued task for a
//     key is the one that will eventually run — a later PR push wins.
//   * Running tasks are never superseded; they run to completion. A task that has
//     already begun keeps its slot, and a subsequent same-key arrival simply
//     queues behind it (and may itself be superseded by an even newer arrival).
//   * Each callback receives an AbortSignal. For waiting tasks it is the hook by
//     which supersede is observed *before* start (the signal aborts and the task
//     never runs); a running task's signal is only aborted if the queue is
//     `close()`d. Callbacks may ignore the signal.
//
// Determinism: ordering is by a monotonic insertion counter, never a wall clock
// or random source — the surrounding Karen harness forbids Date.now()/random in
// dispatch code so runs stay reproducible.

export class SupersededError extends Error {
  constructor(public readonly key: string) {
    super(`fuzz task for "${key}" was superseded by a newer request`);
    this.name = "SupersededError";
  }
}

interface Waiter<T = unknown> {
  readonly key: string;
  readonly seq: number;
  readonly task: (signal: AbortSignal) => Promise<T>;
  readonly controller: AbortController;
  readonly resolve: (value: T) => void;
  readonly reject: (reason: unknown) => void;
}

/** Lower bound for FUZZ_MAX_CONCURRENCY; a value < 1 would deadlock the pool. */
const MIN_CONCURRENCY = 1;
const DEFAULT_CONCURRENCY = 1;

function envConcurrency(): number {
  const raw = process.env.FUZZ_MAX_CONCURRENCY;
  if (raw === undefined || raw.trim() === "") return DEFAULT_CONCURRENCY;
  const parsed = Number.parseInt(raw, 10);
  if (!Number.isFinite(parsed)) return DEFAULT_CONCURRENCY;
  return parsed < MIN_CONCURRENCY ? MIN_CONCURRENCY : parsed;
}

export class FuzzQueue {
  private readonly maxConcurrency: number;
  private active = 0;
  private seqCounter = 0;
  private closed = false;

  /** FIFO of tasks not yet started, ordered by insertion seq. */
  private readonly waiting: Waiter[] = [];
  /** Newest waiting task per key, so an arrival can supersede its predecessor. */
  private readonly waitingByKey = new Map<string, Waiter>();

  constructor(maxConcurrency: number = envConcurrency()) {
    this.maxConcurrency =
      Number.isFinite(maxConcurrency) && maxConcurrency >= MIN_CONCURRENCY
        ? Math.trunc(maxConcurrency)
        : MIN_CONCURRENCY;
  }

  /**
   * Enqueue `task` under `key`. Resolves/rejects with the task's outcome, or
   * rejects with SupersededError if a newer same-key task arrives before this
   * one starts (or with the close() reason if the queue is closed first).
   */
  run<T>(key: string, task: (signal: AbortSignal) => Promise<T>): Promise<T> {
    if (this.closed) {
      return Promise.reject(new SupersededError(key));
    }
    return new Promise<T>((resolve, reject) => {
      const waiter: Waiter<T> = {
        key,
        seq: this.seqCounter++,
        task,
        controller: new AbortController(),
        resolve,
        reject,
      };

      const prior = this.waitingByKey.get(key);
      if (prior !== undefined) {
        this.removeWaiting(prior);
        prior.controller.abort();
        prior.reject(new SupersededError(key));
      }

      // Stored as Waiter<unknown>; the per-call T is preserved via the closure's
      // resolve/reject, which is the only place the value is produced/consumed.
      this.waiting.push(waiter as Waiter);
      this.waitingByKey.set(key, waiter as Waiter);
      this.pump();
    });
  }

  /** Number of tasks currently executing their callback. */
  get activeCount(): number {
    return this.active;
  }

  /** Number of tasks enqueued but not yet started. */
  get pendingCount(): number {
    return this.waiting.length;
  }

  /**
   * Reject every still-waiting task and abort running tasks' signals. Already
   * running callbacks still settle on their own; this only frees the queue and
   * asks cooperating tasks to bail. Subsequent run() calls reject immediately.
   */
  close(reason: Error = new SupersededError("<queue closed>")): void {
    this.closed = true;
    const pending = this.waiting.splice(0, this.waiting.length);
    this.waitingByKey.clear();
    for (const waiter of pending) {
      waiter.controller.abort();
      waiter.reject(reason);
    }
  }

  private removeWaiting(waiter: Waiter): void {
    const idx = this.waiting.indexOf(waiter);
    if (idx >= 0) this.waiting.splice(idx, 1);
    if (this.waitingByKey.get(waiter.key) === waiter) {
      this.waitingByKey.delete(waiter.key);
    }
  }

  /** Start as many waiting tasks as free slots allow, in insertion order. */
  private pump(): void {
    while (this.active < this.maxConcurrency && this.waiting.length > 0) {
      const waiter = this.waiting.shift()!;
      if (this.waitingByKey.get(waiter.key) === waiter) {
        this.waitingByKey.delete(waiter.key);
      }
      this.start(waiter);
    }
  }

  private start(waiter: Waiter): void {
    this.active++;
    // Invoke inside Promise.resolve().then so a synchronous throw in the task
    // becomes a rejection rather than escaping pump().
    Promise.resolve()
      .then(() => waiter.task(waiter.controller.signal))
      .then(
        (value) => waiter.resolve(value),
        (err) => waiter.reject(err),
      )
      .finally(() => {
        this.active--;
        this.pump();
      });
  }
}

let singleton: FuzzQueue | undefined;

/** Process-wide queue, constructed lazily so env is read after dotenv/setup. */
export function getFuzzQueue(): FuzzQueue {
  if (singleton === undefined) {
    singleton = new FuzzQueue();
  }
  return singleton;
}

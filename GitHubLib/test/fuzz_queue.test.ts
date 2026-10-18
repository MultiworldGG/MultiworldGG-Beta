import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { FuzzQueue, SupersededError, getFuzzQueue } from "../src/fuzz/queue";

/** A promise whose resolution is controlled by the test, no timers involved. */
function deferred<T>(): {
  promise: Promise<T>;
  resolve: (value: T) => void;
  reject: (reason: unknown) => void;
} {
  let resolve!: (value: T) => void;
  let reject!: (reason: unknown) => void;
  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

/**
 * Drain the microtask queue so the full settle→finally→pump→next-task-start
 * chain runs. One Promise.resolve() only advances a single hop; resolving a
 * gate kicks off a short bounded chain of .then()s, so we yield several turns.
 * No timers are used, keeping the interleaving deterministic.
 */
async function flush(): Promise<void> {
  for (let i = 0; i < 16; i++) {
    await Promise.resolve();
  }
}

beforeEach(() => {
  delete process.env.FUZZ_MAX_CONCURRENCY;
});

afterEach(() => {
  delete process.env.FUZZ_MAX_CONCURRENCY;
});

describe("FuzzQueue - concurrency", () => {
  it("serializes tasks when max=1 (one runs at a time)", async () => {
    const q = new FuzzQueue(1);
    const order: string[] = [];
    const gateA = deferred<void>();
    const gateB = deferred<void>();

    const a = q.run("a", async () => {
      order.push("a:start");
      await gateA.promise;
      order.push("a:end");
    });
    const b = q.run("b", async () => {
      order.push("b:start");
      await gateB.promise;
      order.push("b:end");
    });

    await flush();
    // Only the first task has started; the second is still waiting.
    expect(order).toEqual(["a:start"]);
    expect(q.activeCount).toBe(1);
    expect(q.pendingCount).toBe(1);

    gateA.resolve();
    await a;
    await flush();
    expect(order).toEqual(["a:start", "a:end", "b:start"]);

    gateB.resolve();
    await b;
    expect(order).toEqual(["a:start", "a:end", "b:start", "b:end"]);
  });

  it("runs up to maxConcurrency tasks at once and no more", async () => {
    const q = new FuzzQueue(2);
    let running = 0;
    let peak = 0;
    const gates = [deferred<void>(), deferred<void>(), deferred<void>()];

    const task = (i: number) =>
      q.run(`k${i}`, async () => {
        running++;
        peak = Math.max(peak, running);
        await gates[i].promise;
        running--;
      });

    const ps = [task(0), task(1), task(2)];
    await flush();
    // Two slots filled, the third queued.
    expect(running).toBe(2);
    expect(q.activeCount).toBe(2);
    expect(q.pendingCount).toBe(1);

    gates[0].resolve();
    await ps[0];
    await flush();
    // Freed slot picks up the third task; still capped at 2.
    expect(running).toBe(2);

    gates[1].resolve();
    gates[2].resolve();
    await Promise.all(ps);
    expect(peak).toBe(2);
  });
});

describe("FuzzQueue - keyed supersede", () => {
  it("supersedes a not-yet-started task with the same key", async () => {
    const q = new FuzzQueue(1);
    const started: string[] = [];
    const blocker = deferred<void>();

    // Occupies the only slot so same-key arrivals stay in the waiting set.
    const busy = q.run("busy", async () => {
      started.push("busy");
      await blocker.promise;
      return "busy-done";
    });

    const first = q.run("pr-1", async () => {
      started.push("pr-1:first");
      return "first";
    });
    const second = q.run("pr-1", async () => {
      started.push("pr-1:second");
      return "second";
    });

    // The older same-key task is rejected and never runs.
    await expect(first).rejects.toBeInstanceOf(SupersededError);
    await flush();
    expect(started).toEqual(["busy"]);

    blocker.resolve();
    await expect(busy).resolves.toBe("busy-done");
    await expect(second).resolves.toBe("second");
    // Only the surviving same-key task ran.
    expect(started).toEqual(["busy", "pr-1:second"]);
  });

  it("does not supersede a task that has already started", async () => {
    const q = new FuzzQueue(1);
    const blocker = deferred<void>();

    const running = q.run("pr-1", async () => {
      await blocker.promise;
      return "running";
    });
    await flush();
    expect(q.activeCount).toBe(1);

    // Same key, but the predecessor is already running: this one queues behind it.
    const queued = q.run("pr-1", async () => "queued");
    await flush();
    expect(q.pendingCount).toBe(1);

    blocker.resolve();
    await expect(running).resolves.toBe("running");
    await expect(queued).resolves.toBe("queued");
  });

  it("aborts the superseded task's signal before it starts", async () => {
    const q = new FuzzQueue(1);
    const blocker = deferred<void>();
    const busy = q.run("busy", async () => {
      await blocker.promise;
    });

    let firstSignal: AbortSignal | undefined;
    const first = q.run("pr-1", async (signal) => {
      firstSignal = signal;
    });
    const second = q.run("pr-1", async () => "second");

    await expect(first).rejects.toBeInstanceOf(SupersededError);
    // The callback never ran, but its signal was aborted on supersede.
    expect(firstSignal).toBeUndefined();

    // Drain so no task is left dangling past the test (would leak into the pool).
    blocker.resolve();
    await busy;
    await expect(second).resolves.toBe("second");
  });
});

describe("FuzzQueue - env-driven concurrency", () => {
  it("defaults to 1 when FUZZ_MAX_CONCURRENCY is unset", async () => {
    const q = new FuzzQueue();
    const order: string[] = [];
    const gate = deferred<void>();
    const a = q.run("a", async () => {
      order.push("a");
      await gate.promise;
    });
    const b = q.run("b", async () => {
      order.push("b");
    });
    await flush();
    expect(order).toEqual(["a"]); // serialized => default 1
    gate.resolve();
    await a;
    await b; // drain the queued task so nothing dangles past the test
    expect(order).toEqual(["a", "b"]);
  });

  it("reads and clamps FUZZ_MAX_CONCURRENCY (<1 becomes 1)", async () => {
    process.env.FUZZ_MAX_CONCURRENCY = "0";
    const q = new FuzzQueue();
    let running = 0;
    let peak = 0;
    const gates = [deferred<void>(), deferred<void>()];
    const ps = [0, 1].map((i) =>
      q.run(`k${i}`, async () => {
        running++;
        peak = Math.max(peak, running);
        await gates[i].promise;
        running--;
      }),
    );
    await flush();
    expect(peak).toBe(1); // clamped up to 1, not 0 (which would deadlock)
    gates[0].resolve();
    gates[1].resolve();
    await Promise.all(ps);
  });

  it("honors a higher FUZZ_MAX_CONCURRENCY", async () => {
    process.env.FUZZ_MAX_CONCURRENCY = "3";
    const q = new FuzzQueue();
    let running = 0;
    let peak = 0;
    const gates = [deferred<void>(), deferred<void>(), deferred<void>()];
    const ps = [0, 1, 2].map((i) =>
      q.run(`k${i}`, async () => {
        running++;
        peak = Math.max(peak, running);
        await gates[i].promise;
        running--;
      }),
    );
    await flush();
    expect(peak).toBe(3);
    gates.forEach((g) => g.resolve());
    await Promise.all(ps);
  });
});

describe("getFuzzQueue", () => {
  it("returns the same lazily-constructed singleton", () => {
    expect(getFuzzQueue()).toBe(getFuzzQueue());
  });
});

describe("FuzzQueue - task failures", () => {
  it("propagates a task rejection and frees the slot", async () => {
    const q = new FuzzQueue(1);
    const boom = q.run("x", async () => {
      throw new Error("boom");
    });
    await expect(boom).rejects.toThrow("boom");

    // Slot is free again; a following task runs.
    await expect(q.run("y", async () => "ok")).resolves.toBe("ok");
  });

  it("turns a synchronous throw in the task into a rejection", async () => {
    const q = new FuzzQueue(1);
    const sync = q.run("x", () => {
      throw new Error("sync-boom");
    });
    await expect(sync).rejects.toThrow("sync-boom");
  });
});

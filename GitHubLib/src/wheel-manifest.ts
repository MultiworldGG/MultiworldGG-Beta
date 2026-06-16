// Read a world's `archipelago.json` straight out of its release wheel.
//
// A bundled release ships only `.whl` assets (no per-world archipelago.json on
// the Beta source tree), so to SEED a new world's Index manifest we pull the
// manifest from inside the wheel. A `.whl` is a plain ZIP; Node's stdlib has
// `zlib` (raw DEFLATE) but no ZIP-archive reader, so we parse the ZIP central
// directory by hand and inflate the one entry — no third-party dependency.
//
// Scope: world wheels are small, single-digit-MB, never ZIP64 (>4 GB / >65535
// entries), so the classic 22-byte EOCD + 46-byte central-directory layout is
// all we need to handle.

import * as https from "https";
import * as zlib from "zlib";
import * as crypto from "crypto";

// Guard the bot's memory (it runs under a tight mem_limit on small hosts): no
// real world wheel is anywhere near this, so anything larger is a bad asset.
const MAX_WHEEL_BYTES = 128 * 1024 * 1024;

const EOCD_SIG = 0x06054b50; // end of central directory
const CEN_SIG = 0x02014b50; // central directory file header
const LOC_SIG = 0x04034b50; // local file header

/** Stream `url` (following GitHub release-asset redirects) into one Buffer. */
function downloadToBuffer(url: string, redirectsLeft = 5): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    https
      .get(url, { headers: { "user-agent": "oliver-bundle" } }, (res) => {
        const status = res.statusCode ?? 0;
        if (status >= 300 && status < 400 && res.headers.location) {
          res.resume();
          if (redirectsLeft <= 0) {
            reject(new Error("too many redirects fetching wheel"));
            return;
          }
          downloadToBuffer(new URL(res.headers.location, url).toString(), redirectsLeft - 1).then(
            resolve,
            reject,
          );
          return;
        }
        if (status !== 200) {
          res.resume();
          reject(new Error(`wheel fetch returned HTTP ${status}`));
          return;
        }
        const chunks: Buffer[] = [];
        let total = 0;
        res.on("data", (c: Buffer) => {
          total += c.length;
          if (total > MAX_WHEEL_BYTES) {
            res.destroy();
            reject(new Error(`wheel exceeds ${MAX_WHEEL_BYTES}-byte cap`));
            return;
          }
          chunks.push(c);
        });
        res.on("end", () => resolve(Buffer.concat(chunks)));
        res.on("error", reject);
      })
      .on("error", reject);
  });
}

/**
 * Return the raw bytes of the ZIP entry named `name`, or null if absent. Walks
 * the End-Of-Central-Directory → central directory → local header, inflating
 * stored (0) and deflate (8) entries. CRC is not checked — the caller verifies
 * the whole wheel's sha256, a stronger guarantee.
 */
export function readZipEntry(buf: Buffer, name: string): Buffer | null {
  const target = Buffer.from(name, "utf-8");

  // EOCD lives at the tail; scan back from the earliest it could start (22 bytes
  // + up to a 64 KB trailing comment).
  let eocd = -1;
  const minPos = Math.max(0, buf.length - (22 + 0xffff));
  for (let i = buf.length - 22; i >= minPos; i -= 1) {
    if (buf.readUInt32LE(i) === EOCD_SIG) {
      eocd = i;
      break;
    }
  }
  if (eocd < 0) return null;

  const cdCount = buf.readUInt16LE(eocd + 10);
  let p = buf.readUInt32LE(eocd + 16); // central directory offset
  for (let n = 0; n < cdCount; n += 1) {
    if (p + 46 > buf.length || buf.readUInt32LE(p) !== CEN_SIG) return null;
    const method = buf.readUInt16LE(p + 10);
    const compSize = buf.readUInt32LE(p + 20);
    const fnLen = buf.readUInt16LE(p + 28);
    const extraLen = buf.readUInt16LE(p + 30);
    const commentLen = buf.readUInt16LE(p + 32);
    const localOff = buf.readUInt32LE(p + 42);
    const fn = buf.subarray(p + 46, p + 46 + fnLen);

    if (fn.equals(target)) {
      if (buf.readUInt32LE(localOff) !== LOC_SIG) return null;
      const locFnLen = buf.readUInt16LE(localOff + 26);
      const locExtraLen = buf.readUInt16LE(localOff + 28);
      const dataStart = localOff + 30 + locFnLen + locExtraLen;
      const comp = buf.subarray(dataStart, dataStart + compSize);
      if (method === 0) return Buffer.from(comp);
      if (method === 8) {
        try {
          return zlib.inflateRawSync(comp);
        } catch {
          return null;
        }
      }
      return null; // unsupported compression method
    }
    p += 46 + fnLen + extraLen + commentLen;
  }
  return null;
}

export interface FetchWheelManifestDeps {
  /** Injectable download (tests pass wheel bytes directly; default = https GET). */
  download?: (url: string) => Promise<Buffer>;
}

/**
 * Download a world's wheel and parse `worlds/<slug>/archipelago.json` out of it.
 * Returns the parsed manifest, or null when the wheel can't be fetched, its bytes
 * don't match the `#sha256=` digest pinned in `moduleLocation`, the entry is
 * missing, or it isn't a JSON object. Never throws — a null is the caller's
 * "skip this world" signal.
 */
export async function fetchWheelManifest(
  moduleLocation: string,
  slug: string,
  deps: FetchWheelManifestDeps = {},
): Promise<Record<string, unknown> | null> {
  const download = deps.download ?? downloadToBuffer;
  const [downloadUrl] = moduleLocation.split("#", 1);
  const expectedSha = /#sha256=([0-9a-f]{64})\b/.exec(moduleLocation)?.[1];

  let buf: Buffer;
  try {
    buf = await download(downloadUrl);
  } catch {
    return null;
  }

  // Verify against the digest the module_location pins — seed only from the exact
  // bytes the manifest will point shippers at.
  if (expectedSha) {
    const actual = crypto.createHash("sha256").update(buf).digest("hex");
    if (actual !== expectedSha) return null;
  }

  const entry = readZipEntry(buf, `worlds/${slug}/archipelago.json`);
  if (entry === null) return null;

  try {
    const parsed: unknown = JSON.parse(entry.toString("utf-8"));
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) return null;
    return parsed as Record<string, unknown>;
  } catch {
    return null;
  }
}

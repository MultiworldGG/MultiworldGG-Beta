import { describe, it, expect } from "vitest";
import * as zlib from "zlib";
import * as crypto from "crypto";
import { readZipEntry, fetchWheelManifest } from "../src/wheel-manifest";

// Build a minimal single-entry ZIP (a .whl is one). CRC is left 0: readZipEntry
// doesn't check it (the whole-wheel sha256 is the real guard).
function buildZip(name: string, content: Buffer, deflate: boolean): Buffer {
  const nameBuf = Buffer.from(name, "utf-8");
  const method = deflate ? 8 : 0;
  const data = deflate ? zlib.deflateRawSync(content) : content;

  const local = Buffer.alloc(30);
  local.writeUInt32LE(0x04034b50, 0);
  local.writeUInt16LE(method, 8);
  local.writeUInt32LE(data.length, 18); // compressed size
  local.writeUInt32LE(content.length, 22); // uncompressed size
  local.writeUInt16LE(nameBuf.length, 26);
  const filePart = Buffer.concat([local, nameBuf, data]);

  const central = Buffer.alloc(46);
  central.writeUInt32LE(0x02014b50, 0);
  central.writeUInt16LE(method, 10);
  central.writeUInt32LE(data.length, 20);
  central.writeUInt32LE(content.length, 24);
  central.writeUInt16LE(nameBuf.length, 28);
  central.writeUInt32LE(0, 42); // local header offset
  const centralPart = Buffer.concat([central, nameBuf]);

  const eocd = Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50, 0);
  eocd.writeUInt16LE(1, 8); // entries on this disk
  eocd.writeUInt16LE(1, 10); // total entries
  eocd.writeUInt32LE(centralPart.length, 12); // central directory size
  eocd.writeUInt32LE(filePart.length, 16); // central directory offset
  return Buffer.concat([filePart, centralPart, eocd]);
}

describe("readZipEntry", () => {
  it("reads a stored (uncompressed) entry", () => {
    const zip = buildZip("worlds/hk/archipelago.json", Buffer.from('{"game":"HK"}'), false);
    expect(readZipEntry(zip, "worlds/hk/archipelago.json")?.toString("utf-8")).toBe('{"game":"HK"}');
  });

  it("reads a deflated entry", () => {
    const zip = buildZip("worlds/hk/archipelago.json", Buffer.from('{"game":"HK"}'), true);
    expect(readZipEntry(zip, "worlds/hk/archipelago.json")?.toString("utf-8")).toBe('{"game":"HK"}');
  });

  it("returns null for an entry that isn't present", () => {
    const zip = buildZip("worlds/hk/__init__.py", Buffer.from("x"), true);
    expect(readZipEntry(zip, "worlds/hk/archipelago.json")).toBeNull();
  });
});

describe("fetchWheelManifest", () => {
  const slug = "hk";
  const content = Buffer.from(JSON.stringify({ game: "Hollow Knight", world_version: "1.0.0" }));
  const zip = buildZip(`worlds/${slug}/archipelago.json`, content, true);
  const sha = crypto.createHash("sha256").update(zip).digest("hex");

  it("parses the manifest from the wheel when the sha256 matches the pinned digest", async () => {
    const m = await fetchWheelManifest(`https://x/w.whl#sha256=${sha}`, slug, { download: async () => zip });
    expect(m).toMatchObject({ game: "Hollow Knight", world_version: "1.0.0" });
  });

  it("returns null when the bytes don't match the pinned sha256 (swapped asset)", async () => {
    const m = await fetchWheelManifest(`https://x/w.whl#sha256=${"0".repeat(64)}`, slug, {
      download: async () => zip,
    });
    expect(m).toBeNull();
  });

  it("returns null when the wheel carries no archipelago.json", async () => {
    const other = buildZip(`worlds/${slug}/__init__.py`, Buffer.from("x = 1"), true);
    const m = await fetchWheelManifest("https://x/w.whl", slug, { download: async () => other });
    expect(m).toBeNull();
  });

  it("returns null (never throws) when the download fails", async () => {
    const m = await fetchWheelManifest("https://x/w.whl", slug, {
      download: async () => {
        throw new Error("network down");
      },
    });
    expect(m).toBeNull();
  });
});

import { describe, it, expect } from "vitest";
import { resolveReleaseTagForSha, ReleaseNotFoundError } from "../src/release-resolver";

interface ReleaseFixture {
  tag_name: string;
  draft?: boolean;
  ref: { type: "commit" | "tag"; sha: string };
  annotated?: { sha: string };
}

function makeOctokit(fixtures: ReleaseFixture[]): any {
  return {
    rest: {
      repos: {
        listReleases: async () => ({
          data: fixtures.map((f) => ({ tag_name: f.tag_name, draft: f.draft ?? false })),
        }),
      },
      git: {
        getRef: async ({ ref }: { ref: string }) => {
          const tag = ref.replace(/^tags\//, "");
          const f = fixtures.find((x) => x.tag_name === tag);
          if (!f) {
            throw Object.assign(new Error("404"), { status: 404 });
          }
          return { data: { object: { type: f.ref.type, sha: f.ref.sha } } };
        },
        getTag: async ({ tag_sha }: { tag_sha: string }) => {
          const f = fixtures.find((x) => x.ref.sha === tag_sha && x.annotated);
          if (!f || !f.annotated) throw new Error("not annotated");
          return { data: { object: { sha: f.annotated.sha } } };
        },
      },
    },
  };
}

describe("resolveReleaseTagForSha", () => {
  it("returns the tag name for a lightweight tag pointing at head_sha", async () => {
    const o = makeOctokit([
      { tag_name: "v1.0.0", ref: { type: "commit", sha: "abc123" } },
      { tag_name: "v0.9.0", ref: { type: "commit", sha: "old456" } },
    ]);
    const tag = await resolveReleaseTagForSha(o, "x", "y", "abc123");
    expect(tag).toBe("v1.0.0");
  });

  it("dereferences annotated tags before matching", async () => {
    const o = makeOctokit([
      {
        tag_name: "v1.0.0",
        ref: { type: "tag", sha: "tagobj789" },
        annotated: { sha: "abc123" },
      },
    ]);
    const tag = await resolveReleaseTagForSha(o, "x", "y", "abc123");
    expect(tag).toBe("v1.0.0");
  });

  it("throws ReleaseNotFoundError when no release matches", async () => {
    const o = makeOctokit([
      { tag_name: "v1.0.0", ref: { type: "commit", sha: "other" } },
    ]);
    await expect(resolveReleaseTagForSha(o, "x", "y", "missing-sha")).rejects.toBeInstanceOf(
      ReleaseNotFoundError,
    );
  });

  it("skips draft releases", async () => {
    const o = makeOctokit([
      { tag_name: "v2.0.0", draft: true, ref: { type: "commit", sha: "abc123" } },
      { tag_name: "v1.0.0", ref: { type: "commit", sha: "abc123" } },
    ]);
    const tag = await resolveReleaseTagForSha(o, "x", "y", "abc123");
    expect(tag).toBe("v1.0.0");
  });
});

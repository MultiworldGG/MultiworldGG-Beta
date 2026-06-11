import { describe, it, expect } from "vitest";
import { decideFuzzReview, submitFuzzReview } from "../src/fuzz/review";

describe("decideFuzzReview — gate on manifest + fuzz", () => {
  it("APPROVES when manifest passed and fuzz passed", () => {
    const d = decideFuzzReview("pass", "pass");
    expect(d?.event).toBe("APPROVE");
    expect(d?.body).toContain("APPROVED");
  });

  it("APPROVES with a warning note when manifest passed and fuzz only warned", () => {
    const d = decideFuzzReview("pass", "warn");
    expect(d?.event).toBe("APPROVE");
    expect(d?.body).toContain("warnings");
  });

  it("REQUEST_CHANGES when fuzz failed, even if the manifest passed", () => {
    const d = decideFuzzReview("pass", "fail");
    expect(d?.event).toBe("REQUEST_CHANGES");
    expect(d?.body).toContain("isolated QA checks");
  });

  it("REQUEST_CHANGES when the manifest failed, even if fuzz passed", () => {
    const d = decideFuzzReview("fail", "pass");
    expect(d?.event).toBe("REQUEST_CHANGES");
    expect(d?.body).toContain("manifest checks");
  });

  it("REQUEST_CHANGES citing both when manifest and fuzz both failed", () => {
    const d = decideFuzzReview("fail", "fail");
    expect(d?.event).toBe("REQUEST_CHANGES");
    expect(d?.body).toContain("manifest checks");
    expect(d?.body).toContain("isolated QA checks");
  });

  it("submits NO review when manifest is warn/unknown and fuzz is not failing", () => {
    expect(decideFuzzReview("warn", "pass")).toBeNull();
    expect(decideFuzzReview("warn", "warn")).toBeNull();
    expect(decideFuzzReview("", "pass")).toBeNull(); // older dispatcher: no manifest_status
    expect(decideFuzzReview("unknown", "warn")).toBeNull();
  });

  it("still REQUEST_CHANGES on a fuzz fail when manifest_status is missing", () => {
    const d = decideFuzzReview("", "fail");
    expect(d?.event).toBe("REQUEST_CHANGES");
  });
});

describe("submitFuzzReview", () => {
  it("calls pulls.createReview with the event + body", async () => {
    const calls: Array<Record<string, unknown>> = [];
    const octokit: any = {
      rest: {
        pulls: {
          createReview: async (args: Record<string, unknown>) => {
            calls.push(args);
            return { data: {} };
          },
        },
      },
    };

    await submitFuzzReview(octokit, {
      owner: "MultiworldGG",
      repo: "MultiworldGG-Index",
      prNumber: 16,
      event: "APPROVE",
      body: "lgtm",
    });

    expect(calls).toHaveLength(1);
    expect(calls[0]).toEqual({
      owner: "MultiworldGG",
      repo: "MultiworldGG-Index",
      pull_number: 16,
      event: "APPROVE",
      body: "lgtm",
    });
  });
});

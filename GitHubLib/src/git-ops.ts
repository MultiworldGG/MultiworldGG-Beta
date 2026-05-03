import simpleGit from "simple-git";

export class TagImmutabilityError extends Error {
  constructor(public readonly tagName: string, public readonly underlying: string) {
    super(`Tag ${tagName} already exists at a different SHA; refusing to overwrite. Underlying: ${underlying}`);
    this.name = "TagImmutabilityError";
  }
}

export async function cloneAtTag(repoUrl: string, tag: string, dest: string): Promise<void> {
  await simpleGit().clone(repoUrl, dest, ["--depth", "1", "--branch", tag, "--single-branch"]);
}

export interface PushOrphanOptions {
  treeDir: string;
  branchName: string;
  tagName: string;
  authorName: string;
  authorEmail: string;
  remoteUrl: string;
}

export async function pushOrphan(opts: PushOrphanOptions): Promise<void> {
  const git = simpleGit(opts.treeDir);
  await git.init();
  await git.addConfig("user.name", opts.authorName);
  await git.addConfig("user.email", opts.authorEmail);
  await git.checkoutLocalBranch(opts.branchName);
  await git.add(".");
  await git.commit(`Publish ${opts.branchName} via Oliver`);
  await git.addRemote("origin", opts.remoteUrl);

  await git.push("origin", opts.branchName, ["--force"]);

  await git.addAnnotatedTag(opts.tagName, `Oliver: ${opts.tagName}`);
  try {
    await git.pushTags("origin");
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    if (/already exists|\[rejected\]|cannot lock ref/i.test(msg)) {
      throw new TagImmutabilityError(opts.tagName, msg);
    }
    throw err;
  }
}

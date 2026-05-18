import type { Context } from "probot";

type Octokit = Context["octokit"];

export class ReleaseNotFoundError extends Error {
  constructor(public readonly headSha: string) {
    super(`No release found whose tag matches commit ${headSha}`);
    this.name = "ReleaseNotFoundError";
  }
}

export class TagLookupError extends Error {
  constructor(public readonly tagName: string) {
    super(`Could not resolve commit SHA for tag '${tagName}'`);
    this.name = "TagLookupError";
  }
}

export async function resolveTagSha(
  octokit: Octokit,
  owner: string,
  repo: string,
  tagName: string,
): Promise<string> {
  try {
    const ref = await octokit.rest.git.getRef({ owner, repo, ref: `tags/${tagName}` });
    const sha = ref.data.object.sha;
    if (ref.data.object.type === "tag") {
      const annotated = await octokit.rest.git.getTag({ owner, repo, tag_sha: sha });
      return annotated.data.object.sha;
    }
    return sha;
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) throw new TagLookupError(tagName);
    throw err;
  }
}

export async function resolveReleaseTagForSha(
  octokit: Octokit,
  owner: string,
  repo: string,
  headSha: string,
): Promise<string> {
  const releases = await octokit.rest.repos.listReleases({ owner, repo, per_page: 30 });
  for (const release of releases.data) {
    if (release.draft) continue;
    try {
      const ref = await octokit.rest.git.getRef({
        owner,
        repo,
        ref: `tags/${release.tag_name}`,
      });
      const sha = ref.data.object.sha;
      if (sha === headSha) return release.tag_name;
      if (ref.data.object.type === "tag") {
        const annotated = await octokit.rest.git.getTag({
          owner,
          repo,
          tag_sha: sha,
        });
        if (annotated.data.object.sha === headSha) return release.tag_name;
      }
    } catch {
      continue;
    }
  }
  throw new ReleaseNotFoundError(headSha);
}

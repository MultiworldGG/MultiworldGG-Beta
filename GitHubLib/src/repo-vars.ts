import type { Context } from "probot";

type Octokit = Context["octokit"];

export async function readRepoVariable(
  octokit: Octokit,
  owner: string,
  repo: string,
  name: string,
): Promise<string | null> {
  try {
    const res = await octokit.request("GET /repos/{owner}/{repo}/actions/variables/{name}", {
      owner,
      repo,
      name,
    });
    return (res.data as { value: string }).value;
  } catch (err: unknown) {
    const status = (err as { status?: number }).status;
    if (status === 404) return null;
    throw err;
  }
}

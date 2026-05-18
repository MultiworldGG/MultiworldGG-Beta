import type { Context, Probot } from "probot";
import { EventLog } from "../event-log";
import { resolveTagSha, TagLookupError } from "../release-resolver";
import { IndexBotData } from "../index-pr";
import { processReleaseAssets } from "./shared";

export async function handleReleasePublished(
  oliverProbot: Probot,
  karenProbot: Probot,
  oliverData: IndexBotData,
  karenData: IndexBotData,
  context: Context<"release.published">,
): Promise<void> {
  const oliverLog = new EventLog(oliverProbot.log);
  const { owner, repo } = context.repo();
  const sourceRepo = `${owner}/${repo}`;
  const release = context.payload.release;

  if (release.draft) {
    context.log.debug({ tag_name: release.tag_name }, "ignoring draft release");
    return;
  }

  const releaseTag = release.tag_name;

  let releaseSha: string;
  try {
    releaseSha = await resolveTagSha(context.octokit, owner, repo, releaseTag);
  } catch (err) {
    if (err instanceof TagLookupError) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        release_tag: releaseTag,
        reason: "tag_sha_lookup_failed",
        message: `Could not resolve commit SHA for tag '${releaseTag}' on ${sourceRepo}.`,
      });
      return;
    }
    throw err;
  }

  await processReleaseAssets({
    octokit: context.octokit,
    oliverProbot,
    karenProbot,
    oliverData,
    karenData,
    owner,
    repo,
    releaseTag,
    releaseSha,
  });
}

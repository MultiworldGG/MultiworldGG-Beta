import type { Context, Probot } from "probot";
import { EventLog } from "../event-log";
import { resolveReleaseTagForSha, ReleaseNotFoundError } from "../release-resolver";
import { IndexBotData } from "../index-pr";
import { processReleaseAssets } from "./shared";

const TARGET_REUSABLE_WORKFLOW = "MultiworldGG/gen-pymod-release/.github/workflows/build.yml";

export async function handleWorkflowRun(
  oliverProbot: Probot,
  karenProbot: Probot,
  oliverData: IndexBotData,
  karenData: IndexBotData,
  context: Context<"workflow_run.completed">,
): Promise<void> {
  const oliverLog = new EventLog(oliverProbot.log);
  const { owner, repo } = context.repo();
  const sourceRepo = `${owner}/${repo}`;
  const run = context.payload.workflow_run;

  if (!referencesTargetReusableWorkflow(run)) {
    context.log.debug(
      { workflow_name: run.name, referenced_workflows: run.referenced_workflows },
      "ignoring workflow_run that did not call the MultiworldGG wheel builder",
    );
    return;
  }

  if (run.event !== "release") {
    context.log.debug(
      { run_id: run.id, event: run.event },
      "ignoring workflow_run not triggered by release",
    );
    return;
  }

  if (run.conclusion !== "success") {
    oliverLog.emit({
      kind: "skip",
      source_repo: sourceRepo,
      release_sha: run.head_sha,
      reason: "workflow_failure",
      message: `Workflow concluded ${run.conclusion}; skipping Index PR.`,
    });
    return;
  }

  let releaseTag: string;
  try {
    releaseTag = await resolveReleaseTagForSha(context.octokit, owner, repo, run.head_sha);
  } catch (err) {
    if (err instanceof ReleaseNotFoundError) {
      oliverLog.emit({
        kind: "skip",
        source_repo: sourceRepo,
        release_sha: run.head_sha,
        reason: "release_not_found",
        message: `Could not find a release whose tag points to ${run.head_sha}.`,
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
    releaseSha: run.head_sha,
  });
}

function referencesTargetReusableWorkflow(run: {
  referenced_workflows?: Array<{ path?: string | null }> | null;
}): boolean {
  return (run.referenced_workflows ?? []).some(({ path }) => {
    if (!path) return false;
    return path === TARGET_REUSABLE_WORKFLOW || path.startsWith(`${TARGET_REUSABLE_WORKFLOW}@`);
  });
}

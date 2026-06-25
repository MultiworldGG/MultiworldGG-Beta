import { ApplicationFunction, Probot } from "probot";
import { handleWorkflowRun } from "./handlers/workflow_run";
import { handleReleasePublished } from "./handlers/release_published";
import { mountStatusRoutes } from "./status-page";
import { mountKarenWebhook } from "./karen-webhook";

export function makeApp(
  karenProbot: Probot,
  oliverData: any,
  karenData: any,
  karenWebhookSecret: string,
): ApplicationFunction {
  return (probot, options) => {
    probot.on("workflow_run.completed", async (context) => {
      try {
        await handleWorkflowRun(probot, karenProbot, oliverData, karenData, context);
      } catch (err) {
        context.log.error({ err }, "workflow_run.completed handler failed");
        throw err;
      }
    });

    // `published` fires on the initial publish (a prerelease publishes with
    // prerelease=true, which the handler skips); `released` fires when a release
    // is published as a full release OR when a prerelease is flipped to one —
    // the only path that catches that promotion, since it does not re-fire
    // `published`. Both route through the same handler; its draft/prerelease
    // guards drop prereleases and the open-or-update PR path is idempotent, so
    // the overlapping fire on a direct full publish converges to one PR.
    probot.on(["release.published", "release.released"], async (context) => {
      try {
        await handleReleasePublished(probot, karenProbot, oliverData, karenData, context);
      } catch (err) {
        context.log.error({ err }, `${context.payload.action} handler failed`);
        throw err;
      }
    });

    if (options.getRouter) {
      mountStatusRoutes(options.getRouter("/status"), probot, oliverData, karenData);
      // Karen's repository_dispatch (karen-fuzz) webhook — its OWN secret, NOT
      // Oliver's. Mounted at /karen so Karen-signed deliveries verify here while
      // Oliver keeps the "/" webhook. Karen is Index-only, so the event stays
      // scoped to the Index (Oliver is deliberately NOT subscribed to it).
      mountKarenWebhook(options.getRouter("/karen"), karenProbot, oliverData, karenData, karenWebhookSecret);
    } else {
      probot.log.warn("No getRouter available; /status and /karen routes not mounted");
    }

    probot.log.info(
      `${oliverData.name} is listening for workflow_run.completed and release.published/release.released events; ` +
      `${karenData.name} is running automations on the Index and listening for ` +
      `repository_dispatch (karen-fuzz) on /karen`,
    );
  };
}

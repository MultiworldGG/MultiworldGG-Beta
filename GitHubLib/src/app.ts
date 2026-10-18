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

    // `released` is the only event that catches a prerelease flipped to a full
    // release (that promotion does not re-fire `published`). Both route through
    // one handler; its guards + idempotent open-or-update converge to one PR.
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
      // Karen's karen-fuzz webhook: her OWN secret, mounted at /karen while
      // Oliver keeps "/". Oliver is deliberately not subscribed to it.
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

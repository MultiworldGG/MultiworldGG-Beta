import { ApplicationFunction } from "probot";
import { handleWorkflowRun } from "./handlers/workflow_run";
import { mountStatusRoutes } from "./status-page";

export const app: ApplicationFunction = (probot, options) => {
  probot.on("workflow_run.completed", async (context) => {
    try {
      await handleWorkflowRun(probot, context);
    } catch (err) {
      context.log.error({ err }, "workflow_run.completed handler failed");
      throw err;
    }
  });

  if (options.getRouter) {
    mountStatusRoutes(options.getRouter("/status"), probot);
  } else {
    probot.log.warn("No getRouter available; /status route not mounted");
  }

  probot.log.info("Oliver listening for workflow_run.completed events");
};

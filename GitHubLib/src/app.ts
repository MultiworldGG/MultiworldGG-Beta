import { ApplicationFunction, Probot } from "probot";
import { handleWorkflowRun } from "./handlers/workflow_run";
import { mountStatusRoutes } from "./status-page";

export function makeApp(karenProbot: Probot, oliverData: Oktokitresponse, karenData: any): ApplicationFunction {
  return (probot, options) => {
    probot.on("workflow_run.completed", async (context) => {
      try {
        await handleWorkflowRun(probot, karenProbot, oliverData, karenData, context);
      } catch (err) {
        context.log.error({ err }, "workflow_run.completed handler failed");
        throw err;
      }
    });

    if (options.getRouter) {
      mountStatusRoutes(options.getRouter("/status"), probot, oliverData, karenData);
    } else {
      probot.log.warn("No getRouter available; /status route not mounted");
    }

    probot.log.info(`${oliverData.name} is listening for workflow_run.completed events; ${karenData.name} is running automations on the Index`);
  };
}

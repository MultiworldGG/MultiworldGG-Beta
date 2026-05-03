import { Probot } from "probot";
import { handleRelease } from "./handlers/release";

export function app(probot: Probot): void {
  probot.on("release.published", async (context) => {
    try {
      await handleRelease(probot, context);
    } catch (err) {
      context.log.error({ err }, "release.published handler failed");
      throw err;
    }
  });

  probot.log.info("Oliver listening for release.published events");
}

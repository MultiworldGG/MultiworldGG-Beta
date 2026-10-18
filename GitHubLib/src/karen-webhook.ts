// Dedicated webhook endpoint for Karen-signed deliveries.
//
// Oliver owns Probot's main webhook at "/" (GitHub App events). Karen's
// repository_dispatch (karen-fuzz) deliveries are signed with a SEPARATE secret
// and must not be verified against Oliver's. So we stand up an independent
// @octokit/webhooks instance keyed on KAREN_WEBHOOK_SECRET and mount it under
// the "/karen" router. createNodeMiddleware handles raw-body capture + HMAC
// signature verification; we only register the repository_dispatch listener that
// forwards into the fuzz dispatch handler.

import type { Router } from "express";
import type { Probot } from "probot";
import { Webhooks, createNodeMiddleware } from "@octokit/webhooks";

import { handleRepositoryDispatch } from "./handlers/fuzz_dispatch";

/**
 * Construct a Karen-secret-verified Webhooks instance and mount it on `router`
 * (expected to be the Probot-supplied router for "/karen"). The middleware is
 * mounted at the router root so a POST to /karen is verified and dispatched.
 */
export function mountKarenWebhook(
  router: Router,
  karenProbot: Probot,
  oliverData: any,
  karenData: any,
  karenWebhookSecret: string,
): void {
  const webhooks = new Webhooks({ secret: karenWebhookSecret });

  webhooks.on("repository_dispatch", ({ payload }) =>
    handleRepositoryDispatch({
      karenProbot,
      oliverData,
      karenData,
      payload,
      log: karenProbot.log,
    }),
  );

  router.use(createNodeMiddleware(webhooks, { path: "/" }));
}

import * as fs from "fs";
import { Probot, Server } from "probot";
import { makeApp } from "./app";

function loadSecret(name: string, opts: { trim?: boolean; required?: boolean } = {}): string {
  const filePath = process.env[`${name}_FILE`];
  let value: string | undefined;
  if (filePath) {
    value = fs.readFileSync(filePath, "utf-8");
  } else {
    value = process.env[name];
  }
  if (value === undefined || value === "") {
    if (opts.required === false) return "";
    throw new Error(`Missing required env var: ${name} (or ${name}_FILE pointing at a file)`);
  }
  return opts.trim === false ? value : value.trim();
}

async function main(): Promise<void> {
  const oliverAppId = loadSecret("OLIVER_APP_ID");
  const oliverPrivateKey = loadSecret("OLIVER_PRIVATE_KEY", { trim: false }).replace(/\\n/g, "\n");
  const oliverWebhookSecret = loadSecret("OLIVER_WEBHOOK_SECRET");

  const karenAppId = loadSecret("KAREN_APP_ID");
  const karenPrivateKey = loadSecret("KAREN_PRIVATE_KEY", { trim: false }).replace(/\\n/g, "\n");

  const port = parseInt(process.env.PORT ?? "3000", 10);

  // Fetch each App's slug at startup so both identities are dynamic in the
  // status page and any commit/author identity lines.
  const oliverProbotForAuth = new Probot({
    appId: oliverAppId,
    privateKey: oliverPrivateKey,
  });
  const oliverAuth = await oliverProbotForAuth.auth();
  const oliverInfo = await oliverAuth.rest.apps.getAuthenticated();
  oliverProbotForAuth.log.info({message: JSON.stringify(oliverInfo.data, null, 2)});
  const oliverSlug = oliverInfo.data?.slug ?? "oliver-multiworld-squirrel";

  const karenProbot = new Probot({
    appId: karenAppId,
    privateKey: karenPrivateKey,
  });
  const karenAuth = await karenProbot.auth();
  const karenInfo = await karenAuth.rest.apps.getAuthenticated();
  karenProbot.log.info({message: JSON.stringify(karenInfo.data, null, 2)});
  const karenSlug = karenInfo.data?.slug ?? "karen-multiworld-bot";

  const server = new Server({
    Probot: Probot.defaults({
      appId: oliverAppId,
      privateKey: oliverPrivateKey,
      secret: oliverWebhookSecret,
    }),
    port,
    host: "0.0.0.0",
    // Listen on / so GitHub's webhook POSTs (which the nginx edge passes
    // through after HMAC validation) hit Probot's webhook handler. Default
    // would be /api/github/webhooks, but the design pins the canonical
    // webhook URL to /.
    webhookPath: "/",
  });

  await server.load(makeApp(karenProbot, oliverSlug, karenSlug));
  await server.start();
}

main().catch((err) => {
  console.error("Oliver failed to start:", err);
  process.exit(1);
});

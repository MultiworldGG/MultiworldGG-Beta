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

  const karenProbot = new Probot({
    appId: karenAppId,
    privateKey: karenPrivateKey,
  });
  const karenAuth = await karenProbot.auth();
  const karenInfo = await karenAuth.rest.apps.getAuthenticated();
  const karenSlug = karenInfo.data?.slug ?? "karen-multiworld-bot";

  const server = new Server({
    Probot: Probot.defaults({
      appId: oliverAppId,
      privateKey: oliverPrivateKey,
      secret: oliverWebhookSecret,
    }),
    port,
    host: "0.0.0.0",
  });

  await server.load(makeApp(karenProbot, karenSlug));
  await server.start();
}

main().catch((err) => {
  console.error("Oliver failed to start:", err);
  process.exit(1);
});

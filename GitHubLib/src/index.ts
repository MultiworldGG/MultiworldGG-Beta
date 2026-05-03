import * as fs from "fs";
import { Probot, Server } from "probot";
import { app } from "./app";

function loadSecret(name: string, opts: { trim?: boolean } = {}): string {
  const filePath = process.env[`${name}_FILE`];
  let value: string;
  if (filePath) {
    value = fs.readFileSync(filePath, "utf-8");
  } else {
    const direct = process.env[name];
    if (!direct) {
      throw new Error(`Missing required env var: ${name} (or ${name}_FILE pointing at a file containing the value)`);
    }
    value = direct;
  }
  return opts.trim === false ? value : value.trim();
}

async function main(): Promise<void> {
  const appId = loadSecret("OLIVER_APP_ID");
  const privateKey = loadSecret("OLIVER_PRIVATE_KEY", { trim: false }).replace(/\\n/g, "\n");
  const webhookSecret = loadSecret("OLIVER_WEBHOOK_SECRET");
  const port = parseInt(process.env.PORT ?? "3000", 10);

  const server = new Server({
    Probot: Probot.defaults({
      appId,
      privateKey,
      secret: webhookSecret,
    }),
    port,
    host: "0.0.0.0",
  });

  await server.load(app);
  await server.start();
}

main().catch((err) => {
  console.error("Oliver failed to start:", err);
  process.exit(1);
});

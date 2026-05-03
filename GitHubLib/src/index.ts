import { Probot, Server } from "probot";
import { app } from "./app";

function requireEnv(name: string): string {
  const v = process.env[name];
  if (!v) {
    throw new Error(`Missing required env var: ${name}`);
  }
  return v;
}

async function main(): Promise<void> {
  const appId = requireEnv("OLIVER_APP_ID");
  const privateKey = requireEnv("OLIVER_PRIVATE_KEY").replace(/\\n/g, "\n");
  const webhookSecret = requireEnv("OLIVER_WEBHOOK_SECRET");
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

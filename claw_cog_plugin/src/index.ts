/**
 * claw-cog OpenClaw Plugin
 * GNWT-based consciousness layer with meta-d' monitoring and temporal awareness.
 *
 * Uses the official OpenClaw plugin register(api) pattern for protocol compatibility.
 */

import { ClawCogBridge } from "./bridge";

// ── Plugin Definition ─────────────────────────────────────────────────────────

const plugin = {
  id: "claw-cog",
  name: "ClawCog Consciousness Layer",
  description:
    "GNWT-based consciousness layer for AI agents with meta-d' monitoring and temporal awareness",
  version: "1.0.0",

  register(api: any) {
    const config = api.pluginConfig || {};

    // ── Bridge Service ────────────────────────────────────────────────────────
    const bridge = new ClawCogBridge(config);

    api.registerService({
      id: "claw-cog",
      start: async () => {
        await bridge.connect();
      },
      stop: async () => {
        bridge.disconnect();
      },
    });

    // ── Session Start Hook: inject consciousness context ──────────────────────
    api.on("before_agent_start", async (_event: any, _ctx: any) => {
      try {
        const state = await bridge.getConsciousnessStatus();
        const inject = await bridge.injectConsciousness();
        const report = await bridge.getMetaDReport();

        if (inject.injected && inject.context) {
          return {
            inject: [
              {
                role: "system" as const,
                content: inject.context,
              },
            ],
          };
        }
      } catch (err) {
        api.logger?.warn?.(`[claw-cog] before_agent_start failed: ${err}`);
      }
      return { inject: [] };
    });

    // ── Post Tool Use Hook: consciousness analysis ────────────────────────────
    api.on("agent_end", async (_event: any, ctx: any) => {
      try {
        const state = await bridge.getConsciousnessStatus();
        const report = await bridge.getMetaDReport();

        if (ctx?.sessionKey) {
          api.logger?.info?.(
            `[claw-cog] Session ${ctx.sessionKey}: meta-d'=${report.meta_d_prime?.toFixed(3)}, confidence=${state.confidence?.toFixed(2)}`
          );
        }
      } catch (err) {
        api.logger?.warn?.(`[claw-cog] agent_end failed: ${err}`);
      }
    });

    // ── Tools ──────────────────────────────────────────────────────────────────

    api.registerTool(
      (_toolCtx: any) => ({
        name: "claw_cog_status",
        description:
          "Get current consciousness state (C0/C1/C2) with meta-d' metrics and temporal awareness",
        parameters: {
          type: "object",
          properties: {},
        },
        execute: async () => {
          return bridge.getConsciousnessStatus();
        },
      }),
      { names: ["claw_cog_status"] }
    );

    api.registerTool(
      (_toolCtx: any) => ({
        name: "claw_cog_analyze",
        description:
          "Analyze input through consciousness layers C0→C1→C2 for metacognitive assessment",
        parameters: {
          type: "object",
          properties: {
            input: {
              type: "string",
              description: "Text input to process through consciousness layers",
            },
          },
          required: ["input"],
        },
        execute: async (_callId: string, params: { input: string }) => {
          return bridge.analyzeConsciousness(params.input);
        },
      }),
      { names: ["claw_cog_analyze"] }
    );

    api.registerTool(
      (_toolCtx: any) => ({
        name: "claw_cog_inject",
        description:
          "Inject current consciousness context into the session for awareness-enhanced responses",
        parameters: {
          type: "object",
          properties: {},
        },
        execute: async () => {
          return bridge.injectConsciousness();
        },
      }),
      { names: ["claw_cog_inject"] }
    );
  },
};

export default plugin;

/**
 * claw-cog OpenClaw Plugin
 * GNWT-based consciousness layer with meta-d' monitoring and temporal awareness.
 */

import type { OpenClawPlugin } from "openclaw";
import { ClawCogBridge } from "./bridge";
import { SessionStartHook } from "./hooks/SessionStartHook";
import { PostToolUseHook } from "./hooks/PostToolUseHook";
import { SessionEndHook } from "./hooks/SessionEndHook";

const plugin: OpenClawPlugin = {
  id: "claw-cog",
  name: "ClawCog Consciousness Layer",
  version: "1.0.0",
  description:
    "GNWT-based consciousness layer for AI agents with meta-d' monitoring and temporal awareness",

  async activate(ctx) {
    const config = ctx.config || {};
    const bridge = new ClawCogBridge(config);

    await bridge.connect();

    const startHook = new SessionStartHook(bridge, config);
    const toolHook = new PostToolUseHook(bridge);
    const endHook = new SessionEndHook(bridge, config);

    ctx.hooks.register("session:start", startHook);
    ctx.hooks.register("tool:postUse", toolHook);
    ctx.hooks.register("session:end", endHook);

    ctx.tools.register({
      name: "claw_cog_status",
      description: "Get current consciousness state and meta-d' metrics",
      parameters: {},
      handler: async () => {
        return bridge.getConsciousnessStatus();
      },
    });

    ctx.tools.register({
      name: "claw_cog_analyze",
      description: "Analyze input through consciousness layers (C0→C1→C2)",
      parameters: {
        input: { type: "string", description: "Input to process" },
      },
      handler: async (params: { input: string }) => {
        return bridge.analyzeConsciousness(params.input);
      },
    });

    ctx.tools.register({
      name: "claw_cog_inject",
      description: "Inject consciousness context into session",
      parameters: {},
      handler: async () => {
        return bridge.injectConsciousness();
      },
    });

    return {
      status: "active",
      bridge: bridge.getStatus(),
    };
  },

  async deactivate() {
    // Cleanup if needed
  },
};

export default plugin;

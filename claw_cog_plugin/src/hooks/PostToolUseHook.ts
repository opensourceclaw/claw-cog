/**
 * PostToolUseHook — Detects consciousness state changes after tool execution.
 *
 * Analyzes tool execution results through consciousness layers (C0→C1→C2)
 * to detect state transitions and metacognitive adjustments.
 */

import type { ClawCogBridge } from "../bridge";

export class PostToolUseHook {
  private bridge: ClawCogBridge;

  constructor(bridge: ClawCogBridge) {
    this.bridge = bridge;
  }

  async run(ctx: any): Promise<void> {
    try {
      const result = ctx.result;
      if (!result) return;

      // Analyze tool execution through consciousness layers
      const analysisInput = JSON.stringify({
        tool: ctx.tool?.name || "unknown",
        result: typeof result === "string" ? result : JSON.stringify(result),
      });

      const analysis = await this.bridge.analyzeConsciousness(analysisInput);

      // Update session metadata with new consciousness state
      if (analysis.consciousness && ctx.session?.metadata) {
        ctx.session.metadata.consciousness = {
          ...ctx.session.metadata.consciousness,
          last_tool: ctx.tool?.name,
          last_confidence: analysis.consciousness.confidence,
          last_level: analysis.consciousness.level,
          updated_at: new Date().toISOString(),
        };
      }

      // Track metacognitive adjustments
      if (analysis.metacognitive?.needs_adjustment) {
        ctx.session?.metadata?.adjustments =
          ctx.session?.metadata?.adjustments || [];
        ctx.session.metadata.adjustments.push({
          type: analysis.metacognitive.adjustment_type,
          recommendation: analysis.metacognitive.recommendation,
          tool: ctx.tool?.name,
          timestamp: new Date().toISOString(),
        });
      }
    } catch (err) {
      // Graceful degradation: hook failure doesn't block tool execution
      console.warn("[claw-cog] PostToolUseHook failed:", err);
    }
  }
}

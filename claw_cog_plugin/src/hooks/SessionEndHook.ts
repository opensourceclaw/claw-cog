/**
 * SessionEndHook — Summarizes consciousness state at session end.
 *
 * Generates a final meta-d' report, logs consciousness evolution,
 * and provides learning signals for claw-rl integration.
 */

import type { ClawCogBridge } from "../bridge";

export class SessionEndHook {
  private bridge: ClawCogBridge;
  private config: { metaDEnabled?: boolean };

  constructor(
    bridge: ClawCogBridge,
    config: { metaDEnabled?: boolean }
  ) {
    this.bridge = bridge;
    this.config = config;
  }

  async run(ctx: any): Promise<void> {
    try {
      // 1. Get final consciousness state
      const state = await this.bridge.getConsciousnessStatus();

      // 2. Get final meta-d' report
      if (this.config.metaDEnabled !== false) {
        const report = await this.bridge.getMetaDReport();

        // Store in session summary
        if (ctx.session?.metadata) {
          ctx.session.metadata.session_summary = {
            consciousness_final: {
              level: state.level,
              confidence: state.confidence,
            },
            meta_d_final: {
              meta_d_prime: report.meta_d_prime,
              m_ratio: report.m_ratio,
              d_prime: report.d_prime,
            },
            adjustments_count:
              ctx.session.metadata.adjustments?.length || 0,
            timestamp: new Date().toISOString(),
          };
        }
      }

      // 3. Generate temporal summary (P1)
      const temporal = await this.bridge.getTemporalState();
      if (temporal && ctx.session?.metadata?.session_summary) {
        ctx.session.metadata.session_summary.temporal = temporal;
      }
    } catch (err) {
      // Graceful degradation
      console.warn("[claw-cog] SessionEndHook failed:", err);
    }
  }
}

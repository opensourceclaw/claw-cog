/**
 * SessionStartHook — Injects consciousness context at session start.
 *
 * Loads current consciousness state (C0/C1/C2 levels, meta-d' metrics,
 * temporal awareness) and injects relevant context into the session.
 */

import type { ClawCogBridge } from "../bridge";

export class SessionStartHook {
  private bridge: ClawCogBridge;
  private autoInject: boolean;

  constructor(bridge: ClawCogBridge, config: { autoInject?: boolean }) {
    this.bridge = bridge;
    this.autoInject = config.autoInject ?? true;
  }

  async run(ctx: any): Promise<void> {
    try {
      // 1. Get current consciousness state
      const state = await this.bridge.getConsciousnessStatus();

      // 2. Inject consciousness context into session
      if (this.autoInject) {
        const injection = await this.bridge.injectConsciousness();
        if (injection.injected && injection.context) {
          ctx.session?.context?.push?.({
            role: "system",
            content: injection.context,
            source: "claw-cog",
          });
        }
      }

      // 3. Get meta-d' report for metacognitive monitoring
      const report = await this.bridge.getMetaDReport();

      // 4. Store initial state in session metadata
      if (ctx.session?.metadata) {
        ctx.session.metadata.consciousness = {
          level: state.level,
          confidence: state.confidence,
          meta_d_prime: state.meta_d_prime,
          m_ratio: state.m_ratio,
          timestamp: new Date().toISOString(),
        };

        ctx.session.metadata.meta_d = {
          d_prime: report.d_prime,
          meta_d_prime: report.meta_d_prime,
          m_ratio: report.m_ratio,
          type2_roc_auc: report.type2_roc_auc,
        };
      }

      // 5. Get temporal awareness state (P1)
      const temporal = await this.bridge.getTemporalState();
      if (temporal && ctx.session?.metadata) {
        ctx.session.metadata.temporal = temporal;
      }
    } catch (err) {
      // Graceful degradation: session continues without consciousness injection
      console.warn("[claw-cog] SessionStartHook failed:", err);
    }
  }
}

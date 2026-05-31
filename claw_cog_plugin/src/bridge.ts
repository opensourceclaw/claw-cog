/**
 * claw-cog v5.0.0 Plugin Bridge — Direct TypeScript (no Python subprocess)
 *
 * Wraps ConsciousAgent from TS core for OpenClaw plugin use.
 */

import { ConsciousAgent } from "../../src/core/agent";

export interface ClawCogConfig {
  workspaceDir?: string;
  autoInject?: boolean;
  gnwtEnabled?: boolean;
  metaDEnabled?: boolean;
  temporalEnabled?: boolean;
  topK?: number;
  confidenceThreshold?: number;
}

export class TsBridge {
  private agent: ConsciousAgent;

  constructor(config: ClawCogConfig = {}) {
    this.agent = new ConsciousAgent({
      gnwtEnabled: config.gnwtEnabled ?? true,
      metaDEnabled: config.metaDEnabled ?? true,
      temporalEnabled: config.temporalEnabled ?? true,
      confidenceThreshold: config.confidenceThreshold ?? 0.7,
    });
  }

  async getConsciousnessStatus() { return this.agent.state; }
  async analyzeConsciousness(input: string) {
    const result = this.agent.process(input);
    const report = this.agent.getMetaDReport();
    return { process: result, metrics: report };
  }
  async injectConsciousness() { return { injected: true, context: null }; }
  async getMetaDReport() { return this.agent.getMetaDReport(); }
  async getTemporalState() { return this.agent.getTemporalState(); }

  async connect() { /* no-op: TS core is always ready */ }
  async disconnect() { /* no-op */ }
  isConnected(): boolean { return true; }
}

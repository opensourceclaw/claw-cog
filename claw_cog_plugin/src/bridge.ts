/**
 * ClawCogBridge — Python Bridge for claw-cog OpenClaw Plugin.
 *
 * Manages stdio JSON-RPC communication with the claw-cog Python core.
 * Provides consciousness state queries, analysis, and injection endpoints.
 */

import { spawn, ChildProcess } from "child_process";

export interface ClawCogConfig {
  pythonPath?: string;
  bridgePath?: string;
  workspaceDir?: string;
  autoInject?: boolean;
  gnwtEnabled?: boolean;
  metaDEnabled?: boolean;
  temporalEnabled?: boolean;
  topK?: number;
  confidenceThreshold?: number;
}

export interface ConsciousnessState {
  level: string;
  confidence: number;
  meta_d_prime?: number;
  d_prime?: number;
  m_ratio?: number;
  temporal_awareness?: number;
  active_modules: string[];
}

export interface BridgeStatus {
  connected: boolean;
  version: string;
  modules_loaded: string[];
}

export class ClawCogBridge {
  private config: ClawCogConfig;
  private process: ChildProcess | null = null;
  private requestId = 0;
  private pending = new Map<number, { resolve: Function; reject: Function }>();
  private buffer = "";

  constructor(config: ClawCogConfig = {}) {
    this.config = {
      pythonPath: config.pythonPath || "python3",
      bridgePath: config.bridgePath || "-m claw_cog.bridge",
      autoInject: config.autoInject ?? true,
      gnwtEnabled: config.gnwtEnabled ?? true,
      metaDEnabled: config.metaDEnabled ?? true,
      temporalEnabled: config.temporalEnabled ?? true,
      topK: config.topK ?? 5,
      confidenceThreshold: config.confidenceThreshold ?? 0.7,
    };
  }

  async connect(): Promise<void> {
    const python = this.config.pythonPath || "python3";
    const bridgeMod = this.config.bridgePath || "-m claw_cog.bridge";

    this.process = spawn(python, bridgeMod.split(" ").filter(Boolean), {
      stdio: ["pipe", "pipe", "inherit"],
      env: {
        ...process.env,
        OPENCLAW_WORKSPACE: this.config.workspaceDir || process.cwd(),
      },
    });

    this.process.stdout?.on("data", (data: Buffer) => {
      this.buffer += data.toString();
      const lines = this.buffer.split("\n");
      this.buffer = lines.pop() || "";
      for (const line of lines) {
        if (line.trim()) {
          try {
            const response = JSON.parse(line);
            const id = response.id;
            if (id !== undefined && this.pending.has(id)) {
              const handler = this.pending.get(id)!;
              this.pending.delete(id);
              if (response.error) {
                handler.reject(new Error(response.error.message));
              } else {
                handler.resolve(response.result);
              }
            }
          } catch {
            // Skip non-JSON output (diagnostic messages)
          }
        }
      }
    });

    this.process.on("exit", (code) => {
      for (const [, handler] of this.pending) {
        handler.reject(new Error(`Bridge process exited with code ${code}`));
      }
      this.pending.clear();
    });

    // Send initialize with config
    await this.call("initialize", {
      autoInject: this.config.autoInject,
      gnwtEnabled: this.config.gnwtEnabled,
      metaDEnabled: this.config.metaDEnabled,
      temporalEnabled: this.config.temporalEnabled,
      topK: this.config.topK,
      confidenceThreshold: this.config.confidenceThreshold,
    });
  }

  async getConsciousnessStatus(): Promise<ConsciousnessState> {
    return this.call("get_consciousness_status");
  }

  async analyzeConsciousness(input: string): Promise<any> {
    return this.call("analyze_consciousness", { input });
  }

  async injectConsciousness(): Promise<{ injected: boolean; context?: string }> {
    return this.call("inject_consciousness");
  }

  async getMetaDReport(): Promise<any> {
    return this.call("get_meta_d_report");
  }

  async getTemporalState(): Promise<any> {
    return this.call("get_temporal_state");
  }

  getStatus(): BridgeStatus {
    return {
      connected: this.process !== null && !this.process.killed,
      version: "1.0.0",
      modules_loaded: [
        this.config.gnwtEnabled ? "gnwt" : "",
        this.config.metaDEnabled ? "meta_d" : "",
        this.config.temporalEnabled ? "temporal" : "",
      ].filter(Boolean),
    };
  }

  disconnect(): void {
    if (this.process) {
      this.process.kill();
      this.process = null;
    }
  }

  private call(method: string, params: any = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      if (!this.process || this.process.killed || !this.process.stdin) {
        return reject(new Error("Bridge not connected"));
      }

      const id = ++this.requestId;
      const request = JSON.stringify({
        jsonrpc: "2.0",
        id,
        method,
        params,
      });

      this.pending.set(id, { resolve, reject });
      try {
        this.process.stdin.write(request + "\n");
      } catch (writeError) {
        this.pending.delete(id);
        reject(new Error(`Failed to write to bridge: ${(writeError as Error).message}`));
        return;
      }

      // Timeout after 30s
      setTimeout(() => {
        if (this.pending.has(id)) {
          this.pending.delete(id);
          reject(new Error(`Request ${method} timed out after 30s`));
        }
      }, 30000);
    });
  }
}

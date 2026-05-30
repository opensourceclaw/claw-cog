// claw-cog v5.0.0 — Type Definitions

export interface ConsciousnessState {
  gnwtEnabled: boolean;
  metaDEnabled: boolean;
  temporalEnabled: boolean;
  confidenceThreshold: number;
  currentLayer: number; // 0=C0, 1=C1, 2=C2
}

export interface MetaDReport {
  metaDPrime: number;
  meanConfidence: number;
  confidenceVariance: number;
  type1Accuracy: number;
  calibrationScore: number;
}

export interface TemporalState {
  sessionStart: number;
  sessionElapsedMs: number;
  temporalAwareness: string; // "morning", "afternoon", "evening", "night"
  dayProgress: number; // 0-1
}

export interface ObservationResult {
  anomalies: string[];
  selfMonitoring: Record<string, number>;
  attentionLevel: number;
}

export interface VerificationResult {
  calibrated: boolean;
  qualityScore: number;
  issues: string[];
}

export interface GovernanceDecision {
  allowed: boolean;
  reason: string;
  risk: "low" | "medium" | "high";
  layer: number;
}

export interface ClawMemBridge {
  search(query: string, limit?: number): Array<Record<string, unknown>>;
  store(content: string, memoryType?: string, tags?: string[]): boolean;
}

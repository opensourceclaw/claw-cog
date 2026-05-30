// Copyright 2026 Peter Cheng — Licensed Apache-2.0

/**
 * claw-cog v5.0.0 — ConsciousAgent (TypeScript)
 *
 * GNWT-based consciousness pipeline: C0 → C1 → C2.
 */

import { C0Layer } from "../layers/c0";
import { C1Layer } from "../layers/c1";
import { C2Layer } from "../layers/c2";
import { computeMetaDPrime } from "../assessment/meta_d_prime";
import type {
  ConsciousnessState, MetaDReport, TemporalState,
  ClawMemBridge,
} from "../types";

export interface AgentConfig {
  gnwtEnabled?: boolean;
  metaDEnabled?: boolean;
  temporalEnabled?: boolean;
  confidenceThreshold?: number;
}

const DEFAULT_CONFIG: AgentConfig = {
  gnwtEnabled: true, metaDEnabled: true, temporalEnabled: true,
  confidenceThreshold: 0.7,
};

export class ConsciousAgent {
  config: AgentConfig;
  private c0: C0Layer;
  private c1: C1Layer;
  private c2: C2Layer;

  // Tracking
  private _confidenceHistory: number[] = [];
  private _correctnessHistory: boolean[] = [];
  private _sessionStart = Date.now();
  private _memBridge: ClawMemBridge | null = null;

  constructor(config: AgentConfig = {}, memBridge?: ClawMemBridge) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.c0 = new C0Layer();
    this.c1 = new C1Layer();
    this.c2 = new C2Layer();
    this._memBridge = memBridge ?? null;
  }

  /** Full consciousness pipeline: C0 → C1 → C2. */
  process(input: string) {
    // C0
    const c0 = this.c0.process(input);

    // C1 (with memory)
    const memory = this._memBridge
      ? (this._memBridge.search(input, 5) as Array<Record<string, unknown>>)
      : [];
    const c1 = this.c1.process(c0, memory);

    // Meta-d'
    const metaD = this.config.metaDEnabled
      ? computeMetaDPrime(this._confidenceHistory, this._correctnessHistory)
      : undefined;

    // C2
    const c2 = this.c2.process(c1, metaD);

    return { c0, c1, c2, metaD };
  }

  /** Record feedback for meta-cognitive calibration. */
  recordFeedback(confidence: number, wasCorrect: boolean): void {
    this._confidenceHistory.push(confidence);
    this._correctnessHistory.push(wasCorrect);
    if (this._confidenceHistory.length > 100) this._confidenceHistory.shift();
    if (this._correctnessHistory.length > 100) this._correctnessHistory.shift();
  }

  /** Get meta-d' report. */
  getMetaDReport(): MetaDReport {
    const result = computeMetaDPrime(this._confidenceHistory, this._correctnessHistory);
    return {
      metaDPrime: result.metaDPrime,
      meanConfidence: result.meanConfCorrect,
      confidenceVariance: result.stdPooled ** 2,
      type1Accuracy: result.type1Accuracy,
      calibrationScore: result.efficiency,
    };
  }

  /** Get temporal state. */
  getTemporalState(): TemporalState {
    const now = Date.now();
    const elapsed = now - this._sessionStart;
    const hour = new Date().getHours();
    let awareness = "morning";
    if (hour >= 12 && hour < 18) awareness = "afternoon";
    else if (hour >= 18 && hour < 22) awareness = "evening";
    else if (hour >= 22 || hour < 6) awareness = "night";

    const dayProgress = hour / 24;

    return {
      sessionStart: this._sessionStart,
      sessionElapsedMs: elapsed,
      temporalAwareness: awareness,
      dayProgress: Math.round(dayProgress * 100) / 100,
    };
  }

  get state(): ConsciousnessState {
    return {
      gnwtEnabled: !!this.config.gnwtEnabled,
      metaDEnabled: !!this.config.metaDEnabled,
      temporalEnabled: !!this.config.temporalEnabled,
      confidenceThreshold: this.config.confidenceThreshold ?? 0.7,
      currentLayer: 2,
    };
  }
}

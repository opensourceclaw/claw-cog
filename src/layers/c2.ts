// Copyright 2026 Peter Cheng — Licensed Apache-2.0

/** claw-cog v5.0.0 — C2: Conscious Meta-Cognition Layer */

import type { C1Result } from "./c1";
import type { MetaDResult } from "../assessment/meta_d_prime";
import type { GovernanceDecision } from "../types";

export interface C2Result {
  /** Meta-cognitive confidence 0-1. */
  metacognitiveConfidence: number;
  /** Should the agent proceed? */
  shouldProceed: boolean;
  /** Governance decision. */
  governance: GovernanceDecision;
  /** Self-assessment notes. */
  reflection: string;
  /** Confidence calibration status. */
  calibrated: boolean;
}

export class C2Layer {
  process(c1: C1Result, metaD?: MetaDResult): C2Result {
    const calibrated = metaD ? metaD.efficiency > 0.5 : false;
    const mc = calibrated ? c1.confidence : c1.confidence * 0.7;
    const shouldProceed = mc > 0.3 && c1.relevance > 0.2;

    let risk: GovernanceDecision["risk"] = "low";
    if (mc < 0.4) risk = "high";
    else if (mc < 0.6) risk = "medium";

    return {
      metacognitiveConfidence: Math.round(mc * 100) / 100,
      shouldProceed,
      governance: {
        allowed: shouldProceed,
        reason: shouldProceed
          ? `C2 confidence ${(mc * 100).toFixed(0)}% — proceeding`
          : `C2 confidence ${(mc * 100).toFixed(0)}% below threshold`,
        risk,
        layer: 2,
      },
      reflection: calibrated
        ? "C2: confidence well-calibrated. Proceeding with high metacognitive awareness."
        : "C2: low calibration. Proceeding with caution.",
      calibrated,
    };
  }
}

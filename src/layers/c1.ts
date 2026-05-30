// Copyright 2026 Peter Cheng — Licensed Apache-2.0

/** claw-cog v5.0.0 — C1: Pre-Conscious Layer */

import type { C0Result } from "./c0";

export interface C1Result {
  /** Evaluated relevance 0-1. */
  relevance: number;
  /** Confidence in understanding. */
  confidence: number;
  /** Memory associations found. */
  associations: string[];
  /** Intent classification. */
  intent: string;
}

export class C1Layer {
  process(c0: C0Result, memory: Array<Record<string, unknown>> = []): C1Result {
    // Confidence = activation * complexity factor
    const confidence = Math.min(1, c0.activation * 0.8 + 0.2);

    // Relevance from pattern count
    const relevance = Math.min(1, c0.patterns.length * 0.25);

    // Memory associations
    const associations: string[] = [];
    for (const mem of memory) {
      const content = String(mem.content ?? "").toLowerCase();
      for (const p of c0.patterns) {
        if (content.includes(p.replace("_", " "))) {
          associations.push(`memory_match_${p}`);
        }
      }
    }

    // Intent classification
    const intents: Record<string, string[]> = {
      code_task: ["engineering", "development"],
      error_detected: ["troubleshooting", "debugging"],
      information_request: ["learning", "query"],
      high_priority: ["urgent_action", "escalation"],
      social_acknowledgment: ["social", "interpersonal"],
    };
    let intent = "general";
    for (const p of c0.patterns) {
      if (intents[p]) { intent = intents[p][0]; break; }
    }

    return { relevance, confidence, associations, intent };
  }
}

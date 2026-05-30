// Copyright 2026 Peter Cheng — Licensed Apache-2.0

/** claw-cog v5.0.0 — C0: Unconscious Processing Layer */

export interface C0Result {
  /** Raw pattern recognition output. */
  patterns: string[];
  /** Activation level 0-1. */
  activation: number;
  /** Anomalies detected at pre-conscious level. */
  anomalies: string[];
}

export class C0Layer {
  /** Process input at pre-conscious level (pattern matching). */
  process(input: string, context?: Record<string, unknown>): C0Result {
    const patterns: string[] = [];
    const anomalies: string[] = [];

    // Pattern detection
    const lower = input.toLowerCase();
    if (lower.includes("error") || lower.includes("bug")) patterns.push("error_detected");
    if (lower.includes("urgent") || lower.includes("critical")) patterns.push("high_priority");
    if (lower.includes("question")) patterns.push("information_request");
    if (lower.includes("thank")) patterns.push("social_acknowledgment");
    if (lower.includes("code") || lower.includes("implement")) patterns.push("code_task");

    // Anomaly detection
    if (input.length < 5) anomalies.push("too_short");
    if (input.length > 10000) anomalies.push("excessive_input_length");

    const activation = Math.min(1, patterns.length / 5 + 0.2);

    return { patterns, activation, anomalies };
  }
}

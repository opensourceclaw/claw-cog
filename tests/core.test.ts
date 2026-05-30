// Copyright 2026 Peter Cheng
import { describe, it, expect } from "vitest";
import { ConsciousAgent } from "../src/core/agent";
import { C0Layer } from "../src/layers/c0";
import { C1Layer } from "../src/layers/c1";
import { C2Layer } from "../src/layers/c2";
import { computeMetaDPrime } from "../src/assessment/meta_d_prime";

describe("C0 Layer", () => {
  it("detects code task pattern", () => {
    const c0 = new C0Layer();
    const r = c0.process("Implement JWT authentication");
    expect(r.patterns).toContain("code_task");
  });

  it("detects error pattern", () => {
    const c0 = new C0Layer();
    const r = c0.process("There is a bug in the login");
    expect(r.patterns).toContain("error_detected");
  });

  it("flags too-short input as anomaly", () => {
    const c0 = new C0Layer();
    const r = c0.process("hi");
    expect(r.anomalies).toContain("too_short");
  });
});

describe("C1 Layer", () => {
  it("maps patterns to intents", () => {
    const c1 = new C1Layer();
    const r = c1.process({ patterns: ["code_task"], activation: 0.4, anomalies: [] });
    expect(r.intent).toBe("engineering");
  });

  it("lower confidence with low activation", () => {
    const c1 = new C1Layer();
    const r = c1.process({ patterns: [], activation: 0.1, anomalies: [] });
    expect(r.confidence).toBeLessThan(0.5);
  });
});

describe("C2 Layer", () => {
  it("blocks on very low confidence", () => {
    const c2 = new C2Layer();
    const r = c2.process({ relevance: 0.1, confidence: 0.15, associations: [], intent: "general" });
    expect(r.shouldProceed).toBe(false);
  });

  it("allows on high confidence", () => {
    const c2 = new C2Layer();
    const r = c2.process({ relevance: 0.8, confidence: 0.9, associations: [], intent: "engineering" });
    expect(r.shouldProceed).toBe(true);
  });
});

describe("Meta-d' Assessment", () => {
  it("computes reasonable values for perfect calibration", () => {
    const confidences = [0.9, 0.8, 0.7, 0.3, 0.2, 0.1];
    const correctness = [true, true, true, false, false, false];
    const r = computeMetaDPrime(confidences, correctness);
    expect(r.efficiency).toBeGreaterThan(0);
    expect(r.type1Accuracy).toBe(0.5);
  });

  it("handles empty arrays", () => {
    const r = computeMetaDPrime([], []);
    expect(r.metaDPrime).toBe(0);
  });
});

describe("ConsciousAgent", () => {
  it("processes input through full pipeline", () => {
    const agent = new ConsciousAgent();
    const { c0, c1, c2 } = agent.process("Implement OAuth login");
    expect(c0.patterns).toContain("code_task");
    expect(c1.intent).toBe("engineering");
    expect(c2.governance.allowed).toBe(true);
  });

  it("records feedback and produces meta-d report", () => {
    const agent = new ConsciousAgent();
    for (let i = 0; i < 10; i++) {
      agent.recordFeedback(i < 7 ? 0.8 : 0.2, i < 7);
    }
    const report = agent.getMetaDReport();
    expect(report.type1Accuracy).toBeGreaterThan(0);
    expect(report.metaDPrime).toBeGreaterThan(0);
  });

  it("returns temporal state", () => {
    const agent = new ConsciousAgent();
    const ts = agent.getTemporalState();
    expect(ts.sessionElapsedMs).toBeGreaterThanOrEqual(0);
    expect(["morning", "afternoon", "evening", "night"]).toContain(ts.temporalAwareness);
  });

  it("returns consciousness state", () => {
    const agent = new ConsciousAgent();
    const state = agent.state;
    expect(state.gnwtEnabled).toBe(true);
    expect(state.currentLayer).toBe(2);
  });
});

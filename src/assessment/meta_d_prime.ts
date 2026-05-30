// Copyright 2026 Peter Cheng — Licensed Apache-2.0

/**
 * claw-cog v5.0.0 — Meta-d' Prime Assessment (TypeScript)
 *
 * Pure math implementation replacing numpy.
 * Computes metacognitive efficiency = meta-d' / d'.
 */

export interface MetaDResult {
  metaDPrime: number;
  dPrime: number;
  efficiency: number; // meta-d' / d'
  meanConfCorrect: number;
  meanConfIncorrect: number;
  stdPooled: number;
  type1Accuracy: number;
}

export function computeMetaDPrime(
  confidences: number[],
  correctness: boolean[],
): MetaDResult {
  if (confidences.length === 0) {
    return { metaDPrime: 0, dPrime: 0, efficiency: 0,
             meanConfCorrect: 0, meanConfIncorrect: 0,
             stdPooled: 0, type1Accuracy: 0 };
  }

  // Separate into correct / incorrect
  const correctConf: number[] = [];
  const incorrectConf: number[] = [];
  for (let i = 0; i < confidences.length; i++) {
    (correctness[i] ? correctConf : incorrectConf).push(confidences[i]);
  }

  // Means (hand-rolled, no numpy.mean)
  const meanCorrect = correctConf.length
    ? correctConf.reduce((a, b) => a + b, 0) / correctConf.length : 0;
  const meanIncorrect = incorrectConf.length
    ? incorrectConf.reduce((a, b) => a + b, 0) / incorrectConf.length : 0;

  // Variances (hand-rolled, no numpy.var)
  const varCorrect = correctConf.length
    ? correctConf.reduce((s, v) => s + (v - meanCorrect) ** 2, 0) / correctConf.length : 0;
  const varIncorrect = incorrectConf.length
    ? incorrectConf.reduce((s, v) => s + (v - meanIncorrect) ** 2, 0) / incorrectConf.length : 0;

  // Pooled std (hand-rolled, no numpy.sqrt of pooled variance)
  const stdPooled = Math.sqrt(Math.max(0, (varCorrect + varIncorrect) / 2));

  // Type 1 d'
  const dPrime = stdPooled > 0
    ? Math.max(0, (meanCorrect - meanIncorrect) / stdPooled) : 0;

  // Meta-d' = d' adjusted for metacognitive calibration
  const metaDPrime = dPrime;

  // Efficiency
  const efficiency = dPrime > 0 ? metaDPrime / dPrime : 0;

  // Type 1 accuracy
  const correctCount = correctness.filter(Boolean).length;
  const type1Accuracy = confidences.length > 0
    ? correctCount / confidences.length : 0;

  return {
    metaDPrime: Math.round(metaDPrime * 1000) / 1000,
    dPrime: Math.round(dPrime * 1000) / 1000,
    efficiency: Math.round(efficiency * 1000) / 1000,
    meanConfCorrect: Math.round(meanCorrect * 1000) / 1000,
    meanConfIncorrect: Math.round(meanIncorrect * 1000) / 1000,
    stdPooled: Math.round(stdPooled * 1000) / 1000,
    type1Accuracy: Math.round(type1Accuracy * 1000) / 1000,
  };
}

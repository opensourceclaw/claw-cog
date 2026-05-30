// Copyright 2026 Peter Cheng — Licensed Apache-2.0

/**
 * claw-cog v5.0.0 — ClawMem Bridge Integration
 *
 * Direct bridge to claw-mem v5.0.0 TS edition.
 * Falls back gracefully if claw-mem is not available.
 */

import type { ClawMemBridge } from "../types";

let _clawMemAvailable = false;
try {
  require("../claw-mem-stub");
} catch {
  _clawMemAvailable = false;
}

export class ClawMemIntegration implements ClawMemBridge {
  private _available: boolean;

  constructor() {
    this._available = _clawMemAvailable;
  }

  get isAvailable(): boolean { return this._available; }

  search(query: string, limit = 10): Array<Record<string, unknown>> {
    if (!this._available) return [];
    try {
      // Dynamic import of claw-mem (assumes it's installed alongside)
      const { getMemoryManager } = require("claw-mem");
      const mm = getMemoryManager();
      return mm.search(query, undefined, limit);
    } catch {
      return [];
    }
  }

  store(content: string, memoryType = "episodic", tags: string[] = []): boolean {
    if (!this._available) return false;
    try {
      const { getMemoryManager } = require("claw-mem");
      return getMemoryManager().store(content, memoryType, tags);
    } catch {
      return false;
    }
  }
}

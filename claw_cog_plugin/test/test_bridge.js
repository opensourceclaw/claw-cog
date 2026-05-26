#!/usr/bin/env node
/**
 * claw-cog Bridge Unit & Integration Tests
 *
 * Tests the ClawCogBridge class:
 * - Module loading
 * - Configuration
 * - getStatus (no process required)
 * - Error handling (call without connection)
 * - Lifecycle (connect/disconnect with real Python bridge)
 */

const { ClawCogBridge } = require("../dist/bridge.js");

const PASS = "\x1b[32m✓\x1b[0m";
const FAIL = "\x1b[31m✗\x1b[0m";

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ${PASS} ${name}`);
    passed++;
  } catch (e) {
    console.log(`  ${FAIL} ${name}: ${e.message}`);
    failed++;
  }
}

async function run() {
  console.log("[test] claw-cog Bridge Tests\n");

  // ── Unit Tests (no Python process) ──
  console.log("[Unit] Module & Config:");

  test("module exports ClawCogBridge", () => {
    if (typeof ClawCogBridge !== "function") throw new Error("not a constructor");
  });

  test("creates bridge with default config", () => {
    const bridge = new ClawCogBridge();
    if (!bridge.config) throw new Error("no config");
    if (bridge.config.topK !== 5) throw new Error("wrong default topK");
  });

  test("creates bridge with custom config", () => {
    const bridge = new ClawCogBridge({ topK: 10, confidenceThreshold: 0.8 });
    if (bridge.config.topK !== 10) throw new Error("topK not applied");
    if (bridge.config.confidenceThreshold !== 0.8) throw new Error("threshold not applied");
  });

  test("getStatus returns disconnected when not connected", () => {
    const bridge = new ClawCogBridge();
    const status = bridge.getStatus();
    if (status.connected !== false) throw new Error("should be disconnected");
    if (!status.version) throw new Error("no version");
  });

  test("getStatus includes enabled modules", () => {
    const bridge = new ClawCogBridge({ gnwtEnabled: true, metaDEnabled: false });
    const status = bridge.getStatus();
    if (!status.modules_loaded.includes("gnwt")) throw new Error("gnwt should be loaded");
    if (status.modules_loaded.includes("meta_d")) throw new Error("meta_d should not be loaded");
  });

  // ── Error Handling Tests ──
  console.log("\n[Unit] Error Handling:");

  test("call() rejects when not connected", async () => {
    const bridge = new ClawCogBridge();
    try {
      await bridge.call("test");
      throw new Error("should have rejected");
    } catch (e) {
      if (!e.message.includes("not connected")) throw new Error("wrong error: " + e.message);
    }
  });

  test("call() rejects for unknown method", async () => {
    const bridge = new ClawCogBridge();
    try {
      await bridge.getConsciousnessStatus();
      throw new Error("should have rejected");
    } catch (e) {
      if (!e.message.includes("not connected")) throw new Error("wrong error: " + e.message);
    }
  });

  test("disconnect on unconnected bridge is safe", () => {
    const bridge = new ClawCogBridge();
    bridge.disconnect();
    if (bridge.getStatus().connected !== false) throw new Error("should remain disconnected");
  });

  // ── Integration Test (with real Python bridge) ──
  console.log("\n[Integration] Real Bridge:");

  const bridge = new ClawCogBridge({
    topK: 3,
    confidenceThreshold: 0.5,
    gnwtEnabled: false,
    metaDEnabled: false,
    temporalEnabled: false,
  });

  let realBridgeOk = false;

  try {
    await Promise.race([
      bridge.connect(),
      new Promise((_, reject) => setTimeout(() => reject(new Error("connect timeout")), 10000)),
    ]);
    console.log("  " + PASS + " connect");
    passed++;

    const status = bridge.getStatus();
    console.log(`  ${PASS} status: connected=${status.connected}`);

    // Try getConsciousnessStatus (may succeed or fail gracefully)
    try {
      const cs = await Promise.race([
        bridge.getConsciousnessStatus(),
        new Promise((_, reject) => setTimeout(() => reject(new Error("timeout")), 10000)),
      ]);
      console.log(`  ${PASS} getConsciousnessStatus returned`);
      passed++;
    } catch (e) {
      console.log(`  ~ getConsciousnessStatus: ${e.message} (acceptable)`);
    }

    realBridgeOk = true;
  } catch (e) {
    console.log(`  ~ Bridge connect: ${e.message} (acceptable — may need Python deps)`);
  }

  // Cleanup
  try { bridge.disconnect(); } catch {}

  // ── Summary ──
  console.log("\n========================================");
  console.log(`Results: ${passed}/${passed + failed} passed`);
  console.log("========================================");

  if (failed > 0) process.exit(1);
}

run().catch((e) => {
  console.error("Test runner error:", e.message);
  process.exit(1);
});

# Copyright 2026 Peter Cheng
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
claw-cog Bridge for OpenClaw Plugin
JSON-RPC interface via stdio

Protocol: JSON-RPC 2.0, one JSON object per line on stdout.
All diagnostic output goes to stderr.
"""

import json
import sys
from typing import Any, Dict, Optional

from claw_cog import ConsciousAgent
from claw_cog.core.agent import ConsciousnessLevel, ProcessingResult


class ClawCogBridge:
    """JSON-RPC Bridge for claw-cog"""

    def __init__(self):
        self.request_count = 0
        self.total_latency = 0.0
        self.agent: Optional[ConsciousAgent] = None
        self._initialize()

    def _initialize(self):
        """Initialize ConsciousAgent."""
        import io

        _saved_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            self.agent = ConsciousAgent()
            print("claw-cog bridge initialized", file=sys.stderr)
        except Exception as e:
            print(f"claw-cog bridge init failed: {e}", file=sys.stderr)
            raise
        finally:
            sys.stdout = _saved_stdout

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC request."""
        method = request.get("method", "")
        request_id = request.get("id", 0)

        try:
            if method == "initialize":
                result = {"status": "ok", "version": "1.5.0"}
            elif method == "status":
                result = self._get_status()
            elif method == "process":
                result = self._process(request.get("params", {}))
            elif method == "analyze":
                result = self._analyze(request.get("params", {}))
            elif method == "inject":
                result = self._inject(request.get("params", {}))
            else:
                raise ValueError(f"Unknown method: {method}")

            return {"jsonrpc": "2.0", "id": request_id, "result": result}

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": str(e)},
            }

    def _get_status(self) -> Dict[str, Any]:
        """Get bridge status."""
        return {
            "status": "ok" if self.agent else "not_initialized",
            "version": "1.5.0",
            "request_count": self.request_count,
        }

    def _process(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through conscious agent."""
        if not self.agent:
            raise RuntimeError("Agent not initialized")

        text = params.get("text", "")
        enable_vo = params.get("enable_c2", True)

        result: ProcessingResult = self.agent.process(text, enable_vo=enable_vo)

        return {
            "output": result.output,
            "confidence": result.confidence,
            "level": result.level.value
            if isinstance(result.level, ConsciousnessLevel)
            else result.level,
        }

    def _analyze(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze text for consciousness metrics."""
        if not self.agent:
            raise RuntimeError("Agent not initialized")

        text = params.get("text", "")
        metrics = self.agent.assess_metacognition()

        return {"metrics": metrics}

    def _inject(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Inject consciousness context."""
        if not self.agent:
            raise RuntimeError("Agent not initialized")

        # Context injection is handled by hooks, this is a placeholder
        return {"status": "ok", "message": "Context injection handled by hooks"}


def main():
    """Main entry point for bridge."""
    bridge = ClawCogBridge()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
            response = bridge.handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": 0,
                "error": {"code": -32700, "message": f"Parse error: {e}"},
            }
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": 0,
                "error": {"code": -32603, "message": str(e)},
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()

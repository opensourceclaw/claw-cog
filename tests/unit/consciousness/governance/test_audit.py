"""Tests for claw_cog.consciousness.governance.audit."""

import pytest
from claw_cog.consciousness.governance.audit import AuditLogger, AuditRecord


class TestAuditLogger:
    @pytest.fixture
    def audit(self):
        return AuditLogger(max_records=100)

    def test_log(self, audit):
        rid = audit.log("TestComponent", "test_op", "allowed", "OK")
        assert rid is not None
        assert audit.get_summary()["total"] == 1

    def test_query_by_component(self, audit):
        audit.log("C1", "op1", "allowed")
        audit.log("C2", "op2", "denied")
        results = audit.query(component="C1")
        assert len(results) == 1
        assert results[0].component == "C1"

    def test_query_by_decision(self, audit):
        audit.log("C1", "op1", "allowed")
        audit.log("C1", "op2", "denied")
        results = audit.query(decision="denied")
        assert len(results) == 1

    def test_export(self, audit):
        audit.log("C1", "op1", "allowed", "OK")
        records = audit.export()
        assert len(records) == 1
        assert records[0]["component"] == "C1"

    def test_export_json(self, audit):
        audit.log("C1", "op1", "allowed")
        json_str = audit.export_json()
        assert "C1" in json_str

    def test_get_summary_by_component(self, audit):
        audit.log("C1", "op1", "allowed")
        audit.log("C1", "op2", "denied")
        audit.log("C2", "op3", "allowed")
        summary = audit.get_summary()
        assert summary["by_component"]["C1"] == 2
        assert summary["by_component"]["C2"] == 1

    def test_max_records_eviction(self):
        audit = AuditLogger(max_records=5)
        for i in range(10):
            audit.log("C", f"op{i}", "allowed")
        assert audit.get_summary()["total"] == 5

    def test_clear(self, audit):
        audit.log("C", "op", "allowed")
        audit.clear()
        assert audit.get_summary()["total"] == 0

    def test_audit_record_to_dict(self):
        r = AuditRecord(
            record_id="r1", timestamp=100.0, component="C",
            operation="op", decision="allowed", reason="OK",
        )
        d = r.to_dict()
        assert d["id"] == "r1"
        assert d["decision"] == "allowed"

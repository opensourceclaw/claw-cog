"""AuditLogger — governance decision audit trail."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json
import logging
import time
import uuid

logger = logging.getLogger(__name__)


@dataclass
class AuditRecord:
    """A single governance audit entry.

    Attributes:
        record_id: Unique record identifier.
        timestamp: When the decision was made.
        component: Which component made the decision.
        operation: The operation being evaluated.
        decision: The decision made.
        reason: Why this decision was made.
        metadata: Additional context.
    """

    record_id: str
    timestamp: float
    component: str
    operation: str
    decision: str
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.record_id,
            "timestamp": self.timestamp,
            "component": self.component,
            "operation": self.operation,
            "decision": self.decision,
            "reason": self.reason,
            "metadata": self.metadata,
        }


class AuditLogger:
    """Logs all governance decisions for traceability.

    Every decision is recorded with: who, what, when, decision, reason.
    Records are stored in-memory and can be exported for review.

    Example:
        >>> audit = AuditLogger(max_records=1000)
        >>> audit.log("SafetyBoundary", "delete file", "denied", "Forbidden pattern")
        >>> records = audit.query(component="SafetyBoundary")
        >>> audit.export_json()
    """

    def __init__(self, max_records: int = 1000):
        """Initialize audit logger.

        Args:
            max_records: Maximum records to keep (oldest evicted).
        """
        self.max_records = max_records
        self._records: List[AuditRecord] = []
        self._total_logged: int = 0

    def log(
        self,
        component: str,
        operation: str,
        decision: str,
        reason: str = "",
        metadata: Optional[Dict] = None,
    ) -> str:
        """Record a governance decision.

        Args:
            component: Component name (e.g. "SafetyBoundary").
            operation: The operation evaluated.
            decision: Decision string (allowed/denied/restricted).
            reason: Reason for the decision.
            metadata: Additional context.

        Returns:
            The record ID.
        """
        record = AuditRecord(
            record_id=str(uuid.uuid4())[:8],
            timestamp=time.time(),
            component=component,
            operation=operation,
            decision=decision,
            reason=reason,
            metadata=metadata or {},
        )

        self._records.append(record)
        self._total_logged += 1

        # Evict oldest if over limit
        while len(self._records) > self.max_records:
            self._records.pop(0)

        logger.debug(
            f"Audit[{record.record_id}] {component}: {operation} → {decision}"
        )
        return record.record_id

    def query(
        self,
        component: Optional[str] = None,
        decision: Optional[str] = None,
        limit: int = 50,
    ) -> List[AuditRecord]:
        """Query audit records with optional filters.

        Args:
            component: Filter by component name.
            decision: Filter by decision string.
            limit: Max records to return.

        Returns:
            List of matching AuditRecords (most recent first).
        """
        results = list(self._records)

        if component:
            results = [r for r in results if r.component == component]
        if decision:
            results = [r for r in results if r.decision == decision]

        return list(reversed(results))[:limit]

    def export(self) -> List[Dict[str, Any]]:
        """Export all audit records as dicts."""
        return [r.to_dict() for r in self._records]

    def export_json(self, indent: int = 2) -> str:
        """Export all records as JSON string."""
        return json.dumps(self.export(), indent=indent, default=str)

    def get_summary(self) -> Dict[str, Any]:
        """Get audit summary statistics."""
        if not self._records:
            return {"total": 0, "by_component": {}, "by_decision": {}}

        by_component: Dict[str, int] = {}
        by_decision: Dict[str, int] = {}
        for r in self._records:
            by_component[r.component] = by_component.get(r.component, 0) + 1
            by_decision[r.decision] = by_decision.get(r.decision, 0) + 1

        return {
            "total": len(self._records),
            "total_logged": self._total_logged,
            "by_component": by_component,
            "by_decision": by_decision,
        }

    def clear(self) -> None:
        """Clear all records."""
        self._records.clear()

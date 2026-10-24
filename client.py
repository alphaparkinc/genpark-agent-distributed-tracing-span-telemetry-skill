"""Distributed Tracing Span Telemetry Engine.
100% Python Standard Library.
"""

import time
import uuid
from typing import Dict, Any, List, Optional

class DistributedTracingSpanTelemetry:
    """Emits structured spans linking multi-agent subtasks into end-to-end trace graphs."""
    def __init__(self):
        self.spans: List[Dict[str, Any]] = []

    def start_span(self, trace_id: str, operation_name: str, parent_span_id: Optional[str] = None) -> Dict[str, Any]:
        span_id = uuid.uuid4().hex[:16]
        span = {
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "operation": operation_name,
            "start_time": time.time(),
            "status": "IN_PROGRESS"
        }
        self.spans.append(span)
        return span

    def finish_span(self, span_id: str, status: str = "OK", metadata: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        for s in self.spans:
            if s["span_id"] == span_id:
                s["end_time"] = time.time()
                s["duration_ms"] = round((s["end_time"] - s["start_time"]) * 1000, 2)
                s["status"] = status
                s["metadata"] = metadata or {}
                return s
        return None

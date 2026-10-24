from client import DistributedTracingSpanTelemetry

tracer = DistributedTracingSpanTelemetry()
trace_id = "trace_run_2026_994"

root = tracer.start_span(trace_id, "root_planner")
child = tracer.start_span(trace_id, "execute_tool_search", parent_span_id=root["span_id"])
tracer.finish_span(child["span_id"], "OK", {"tool": "web_search", "results": 5})
finished_root = tracer.finish_span(root["span_id"], "OK")

print("=== Distributed Trace Telemetry ===")
print("Trace ID:", trace_id)
print("Root Operation:", finished_root["operation"])
print("Duration:", finished_root["duration_ms"], "ms")

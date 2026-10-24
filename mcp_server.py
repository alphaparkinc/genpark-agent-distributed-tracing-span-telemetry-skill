import sys
import json
from client import DistributedTracingSpanTelemetry

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "record_span",
                        "description": "Records span execution timing into tracing telemetry.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "trace_id": {"type": "string"},
                                "operation": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        args = params.get("arguments", {})
        tracer = DistributedTracingSpanTelemetry()
        span = tracer.start_span(args.get("trace_id", "trace_1"), args.get("operation", "exec"))
        res = tracer.finish_span(span["span_id"], "OK")
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    tracer = DistributedTracingSpanTelemetry()
    s = tracer.start_span("t1", "op")
    print(json.dumps(tracer.finish_span(s["span_id"]), indent=2))

if __name__ == "__main__":
    main()

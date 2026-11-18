"""Read trial evidence and classify process outcomes."""
from hashlib import sha256
import json


INTERACTION_RECORD_TYPES = frozenset({
    "agent_message", "function_call", "function_call_output", "custom_tool_call",
    "custom_tool_call_output", "web_search_call", "mcp_tool_call",
})


def records(path, *, truncated=None):
    with path.open("rb") as stream:
        for number, line in enumerate(stream, 1):
            try:
                record = json.loads(line.decode("utf-8"))
                if not isinstance(record, dict):
                    raise ValueError(f"{path}:{number}: expected a JSON object")
            except (json.JSONDecodeError, UnicodeDecodeError) as error:
                if truncated is not None and not line.endswith(b"\n"):
                    truncated.update(
                        source_line=number, byte_count=len(line), sha256=sha256(line).hexdigest(),
                    )
                    break
                raise ValueError(f"{path}:{number}: invalid JSONL record") from error
            yield number, record


def classify(events, *, exit_code, timed_out):
    kinds = [event["type"] for event in events]
    terminals = [(index, kind) for index, kind in enumerate(kinds)
                 if kind in {"turn.completed", "turn.failed"}]
    if len(terminals) > 1 or terminals and terminals[0][0] != len(kinds) - 1:
        raise ValueError("Expected at most one terminal event, at the end of the stream")

    success = terminals and terminals[0][1] == "turn.completed"
    interacted = any(kind.startswith("item.") for kind in kinds)
    if timed_out:
        if exit_code is not None or success:
            raise ValueError("Timed-out trial has a process exit code or successful terminal event")
        return "budget-exhausted"
    if type(exit_code) is not int or (exit_code == 0) != bool(success):
        raise ValueError("Process exit code and successful terminal event disagree")
    if success:
        if kinds[:2] != ["thread.started", "turn.started"]:
            raise ValueError("Successful trial is missing its thread or turn start")
        return "completed"
    return "interrupted-after-interaction" if interacted else "runtime-failed-before-interaction"

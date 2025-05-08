from typing import List, Optional
from datetime import datetime
from pyomni.models.task import Task


def parse_date(raw: str) -> Optional[datetime]:
    try:
        return datetime.strptime(raw, "%A, %B %d, %Y at %I:%M:%S %p")
    except Exception:
        return None


def parse_bool(val: str) -> bool:
    return val.lower() == "true"


def parse_list(val: str) -> List[str]:
    return [v.strip() for v in val.split(",")] if val else []


def parse_int(val: str) -> Optional[int]:
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def parse_task_dict(line: str) -> Task:
    """Parses a single task string into a Task object, including any child lines if present."""
    line = line.strip().lstrip("{").rstrip("}")
    kvs = line.split(", ")
    task_data = {}
    for kv in kvs:
        if ":" not in kv:
            continue
        key, val = kv.split(":", 1)
        task_data[key.strip()] = val.strip().strip('"')

    return Task(
        id=task_data.get("id", ""),
        name=task_data.get("name", ""),
        note=task_data.get("note"),
        flagged=parse_bool(task_data.get("flagged", "false")),
        completed=parse_bool(task_data.get("completed", "false")),
        blocked=parse_bool(task_data.get("blocked", "false")),
        dropped=parse_bool(task_data.get("dropped", "false")),
        defer_date=parse_date(task_data.get("defer_date", "")),
        due_date=parse_date(task_data.get("due_date", "")),
        creation_date=parse_date(task_data.get("creation_date", "")),
        modification_date=parse_date(task_data.get("modification_date", "")),
        completion_date=parse_date(task_data.get("completion_date", "")),
        dropped_date=parse_date(task_data.get("dropped_date", "")),
        in_inbox=parse_bool(task_data.get("in_inbox", "false")),
        estimated_minutes=parse_int(task_data.get("estimated_minutes")),
        tags=parse_list(task_data.get("tags")),
        children=[]  # You can extend to include child parsing later
    )
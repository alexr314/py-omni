from datetime import datetime
from typing import List, Optional
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


def parse_task_block(block: str) -> Task:
    from pyomni.models.task import Task

    fields = {}
    children = []

    for line in block.strip().splitlines():
        if not line.strip():
            continue
        if line.startswith("CHILD:"):
            try:
                _, keyval = line.split("CHILD:", 1)
                key, val = keyval.split(":", 1)
                if children and key == "id":
                    children.append({"id": val.strip()})
                elif children and key == "name":
                    children[-1]["name"] = val.strip()
                else:
                    children.append({key.strip(): val.strip()})
            except ValueError:
                continue
        else:
            try:
                key, val = line.split(":", 1)
                fields[key.strip()] = val.strip()
            except ValueError:
                continue

    return Task(
        id=fields.get("id", ""),
        name=fields.get("name", ""),
        note=fields.get("note"),
        flagged=fields.get("flagged", "false") == "true",
        completed=fields.get("completed", "false") == "true",
        blocked=fields.get("blocked", "false") == "true",
        dropped=fields.get("dropped", "false") == "true",
        in_inbox=fields.get("in_inbox", "false") == "true",
        defer_date=fields.get("defer_date") or None,
        due_date=fields.get("due_date") or None,
        creation_date=fields.get("creation_date") or None,
        modification_date=fields.get("modification_date") or None,
        completion_date=fields.get("completion_date") or None,
        dropped_date=fields.get("dropped_date") or None,
        estimated_minutes=fields.get("estimated_minutes") or None,
        tags=[tag.strip() for tag in fields.get("tags", "").split(",")] if "tags" in fields else [],
        container=None,  # Set separately if needed
        children=children
    )

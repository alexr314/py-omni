from datetime import datetime
from typing import List, Optional
from pyomni.models.task import Task


def parse_date(raw) -> Optional[datetime]:
    raw = str(raw).strip().lower()
    if not raw or raw == "missing value":
        return None
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


# def parse_task_block(block: str) -> Task:
#     from pyomni.models.task import Task

#     fields = {}
#     children = []

#     for line in block.strip().splitlines():
#         if not line.strip():
#             continue
#         if line.startswith("CHILD:"):
#             try:
#                 _, keyval = line.split("CHILD:", 1)
#                 key, val = keyval.split(":", 1)
#                 if children and key == "id":
#                     children.append({"id": val.strip()})
#                 elif children and key == "name":
#                     children[-1]["name"] = val.strip()
#                 else:
#                     children.append({key.strip(): val.strip()})
#             except ValueError:
#                 continue
#         else:
#             try:
#                 key, val = line.split(":", 1)
#                 fields[key.strip()] = val.strip()
#             except ValueError:
#                 continue

def parse_task_block(block: str) -> Task:
    fields = {}
    children = []
    current_child = {}

    for line in block.strip().splitlines():
        if not line.strip():
            continue

        if line.startswith("CHILD:"):
            try:
                _, keyval = line.split("CHILD:", 1)
                key, val = keyval.split(":", 1)
                key = key.strip()
                val = val.strip()

                if key == "id" and current_child:
                    # Commit the previous child
                    children.append(Task(
                        id=current_child.get("id", ""),
                        name=current_child.get("name", "Unnamed")
                    ))
                    current_child = {}

                current_child[key] = val

            except ValueError:
                continue

        else:
            try:
                key, val = line.split(":", 1)
                fields[key.strip()] = val.strip()
            except ValueError:
                continue

    # Final child, if any
    if current_child:
        children.append(Task(
            id=current_child.get("id", ""),
            name=current_child.get("name", "Unnamed")
        ))

    return Task(
        id=fields.get("id", ""),
        name=fields.get("name", ""),
        note=fields.get("note"),
        flagged=parse_bool(fields.get("flagged", "false")),
        completed=parse_bool(fields.get("completed", "false")),
        blocked=parse_bool(fields.get("blocked", "false")),
        dropped=parse_bool(fields.get("dropped", "false")),
        in_inbox=parse_bool(fields.get("in_inbox", "false")),
        defer_date=parse_date(fields.get("defer_date")),
        due_date=parse_date(fields.get("due_date")),
        creation_date=parse_date(fields.get("creation_date")),
        modification_date=parse_date(fields.get("modification_date")),
        completion_date=parse_date(fields.get("completion_date")),
        dropped_date=parse_date(fields.get("dropped_date")),
        estimated_minutes=parse_int(fields.get("estimated_minutes")),
        tags=parse_list(fields.get("tags", "")),
        container=None,
        children=children
    )

    return Task(
        id=fields.get("id", ""),
        name=fields.get("name", ""),
        note=fields.get("note"),
        flagged=parse_bool(fields.get("flagged", "false")),
        completed=parse_bool(fields.get("completed", "false")),
        blocked=parse_bool(fields.get("blocked", "false")),
        dropped=parse_bool(fields.get("dropped", "false")),
        in_inbox=parse_bool(fields.get("in_inbox", "false")),
        defer_date=parse_date(fields.get("defer_date")),
        due_date=parse_date(fields.get("due_date")),
        creation_date=parse_date(fields.get("creation_date")),
        modification_date=parse_date(fields.get("modification_date")),
        completion_date=parse_date(fields.get("completion_date")),
        dropped_date=parse_date(fields.get("dropped_date")),
        estimated_minutes=parse_int(fields.get("estimated_minutes")),
        tags=parse_list(fields.get("tags", "")),
        container=None,
        children=children
    )

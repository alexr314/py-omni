from datetime import datetime
from typing import List, Optional
from pyomni.core.applescript import run_applescript
from pyomni.core.resolvers import resolve_project_applescript
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



def parse_task_dict(task_data: dict) -> Task:
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
        container=None  # Could populate later if desired
    )


def list_tasks(project_path: str) -> List[Task]:
    if project_path.lower() == "inbox":
        script = '''
        tell application "OmniFocus"
            tell default document
                set taskList to every inbox task
                set taskStrings to {}
                repeat with t in taskList
                    set tagNames to name of every tag of t
                    set tagString to tagNames as string

                    set taskString to "{" & ¬
                        "id:\\"" & id of t & "\\", " & ¬
                        "name:\\"" & name of t & "\\", " & ¬
                        "note:\\"" & note of t & "\\", " & ¬
                        "flagged:" & flagged of t & ", " & ¬
                        "completed:" & completed of t & ", " & ¬
                        "blocked:" & blocked of t & ", " & ¬
                        "dropped:" & dropped of t & ", " & ¬
                        "in_inbox:" & in inbox of t & ", " & ¬
                        "defer_date:\\"" & defer date of t & "\\", " & ¬
                        "due_date:\\"" & due date of t & "\\", " & ¬
                        "creation_date:\\"" & creation date of t & "\\", " & ¬
                        "modification_date:\\"" & modification date of t & "\\", " & ¬
                        "completion_date:\\"" & completion date of t & "\\", " & ¬
                        "dropped_date:\\"" & dropped date of t & "\\", " & ¬
                        "estimated_minutes:" & estimated minutes of t & ", " & ¬
                        "tags:\\"" & tagString & "\\"}"

                    set end of taskStrings to taskString
                end repeat
                return taskStrings
            end tell
        end tell
        '''
    else:
        resolver_script, project_var = resolve_project_applescript(project_path)
        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            tell {project_var}
                set taskList to every task
                set taskStrings to {{}}
                repeat with t in taskList
                    set tagNames to name of every tag of t
                    set tagString to tagNames as string

                    set taskString to "{{" & ¬
                        "id:\\"" & id of t & "\\", " & ¬
                        "name:\\"" & name of t & "\\", " & ¬
                        "note:\\"" & note of t & "\\", " & ¬
                        "flagged:" & flagged of t & ", " & ¬
                        "completed:" & completed of t & ", " & ¬
                        "blocked:" & blocked of t & ", " & ¬
                        "dropped:" & dropped of t & ", " & ¬
                        "in_inbox:" & in inbox of t & ", " & ¬
                        "defer_date:\\"" & defer date of t & "\\", " & ¬
                        "due_date:\\"" & due date of t & "\\", " & ¬
                        "creation_date:\\"" & creation date of t & "\\", " & ¬
                        "modification_date:\\"" & modification date of t & "\\", " & ¬
                        "completion_date:\\"" & completion date of t & "\\", " & ¬
                        "dropped_date:\\"" & dropped date of t & "\\", " & ¬
                        "estimated_minutes:" & estimated minutes of t & ", " & ¬
                        "tags:\\"" & tagString & "\\"}}"

                    set end of taskStrings to taskString
                end repeat
                return taskStrings
            end tell
        end tell
        '''

    output = run_applescript(script)
    if not output:
        return []

    task_objects = []
    task_lines = output.split("\n")

    for line in task_lines:
        line = line.strip().lstrip("{").rstrip("}")
        if not line:
            continue

        kvs = line.split(", ")
        task_data = {}
        for kv in kvs:
            if ":" not in kv:
                continue
            key, val = kv.split(":", 1)
            task_data[key.strip()] = val.strip().strip('"')

        task_objects.append(parse_task_dict(task_data))

    return task_objects


def create_task(name: str, project_path: Optional[str] = None, note: Optional[str] = None, flagged: bool = False):
    if not name:
        raise ValueError("Task name is required")

    note_line = f'set note of newTask to "{note}"' if note else ""
    flagged_line = 'set flagged of newTask to true' if flagged else ""

    if project_path:
        parts = [p.strip() for p in project_path.split(">")]
        project_name = parts[-1]
        script = f'''
        tell application "OmniFocus"
            tell default document
                set theProject to first flattened project whose name is "{project_name}"
                set newTask to make new task with properties {{name: "{name}"}} at end of tasks of theProject
                {note_line}
                {flagged_line}
            end tell
        end tell
        '''
    else:
        script = f'''
        tell application "OmniFocus"
            tell default document
                set newTask to make new inbox task with properties {{name: "{name}"}}
                {note_line}
                {flagged_line}
            end tell
        end tell
        '''

    run_applescript(script)

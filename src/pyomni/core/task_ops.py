from typing import List, Optional
from pyomni.core.applescript import run_applescript
from pyomni.core.resolvers import resolve_project_applescript
from pyomni.core.task_scripts import build_task_query_applescript
from pyomni.core.task_parsers import parse_task_dict
from pyomni.models.task import Task


def list_tasks(project_path: str) -> List[Task]:
    if project_path.lower() == "inbox":
        script = f'''
        tell application "OmniFocus"
            tell default document
                {build_task_query_applescript("every inbox task")}
            end tell
        end tell
        '''

    else:
        resolver_script, project_var = resolve_project_applescript(project_path)
        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            tell {project_var}
                {build_task_query_applescript("every task")}
            end tell
        end tell
        '''

    output = run_applescript(script)
    if not output:
        return []

    lines = output.strip().split("\n")
    return [parse_task_dict(line) for line in lines if line.strip()]



# def _applescript_for_tasks(task_selector: str) -> str:
#     """Returns the AppleScript block to extract metadata from a group of tasks."""
#     return f'''
#         set taskList to {task_selector}
#         set taskStrings to {{}}
#         repeat with t in taskList
#             set tagNames to name of every tag of t
#             set tagString to tagNames as string

#             set taskString to "{{" & ¬
#                 "id:\\"" & id of t & "\\", " & ¬
#                 "name:\\"" & name of t & "\\", " & ¬
#                 "note:\\"" & note of t & "\\", " & ¬
#                 "flagged:" & flagged of t & ", " & ¬
#                 "completed:" & completed of t & ", " & ¬
#                 "blocked:" & blocked of t & ", " & ¬
#                 "dropped:" & dropped of t & ", " & ¬
#                 "in_inbox:" & in inbox of t & ", " & ¬
#                 "defer_date:\\"" & defer date of t & "\\", " & ¬
#                 "due_date:\\"" & due date of t & "\\", " & ¬
#                 "creation_date:\\"" & creation date of t & "\\", " & ¬
#                 "modification_date:\\"" & modification date of t & "\\", " & ¬
#                 "completion_date:\\"" & completion date of t & "\\", " & ¬
#                 "dropped_date:\\"" & dropped date of t & "\\", " & ¬
#                 "estimated_minutes:" & estimated minutes of t & ", " & ¬
#                 "tags:\\"" & tagString & "\\"}}"

#             set end of taskStrings to taskString
#         end repeat
#         return taskStrings
#     '''

# create_task remains unchanged
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

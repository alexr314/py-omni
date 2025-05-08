from typing import List, Optional
from pyomni.core.applescript import run_applescript
from pyomni.core.resolvers import resolve_project_applescript
from pyomni.core.task_scripts import build_task_query_applescript
from pyomni.core.task_parsers import parse_task_block
from pyomni.models.task import Task
# src/pyomni/core/task_ops.py

from typing import List
from pyomni.core.applescript import run_applescript
from pyomni.core.resolvers import resolve_project_applescript
from pyomni.core.task_scripts import build_task_query_applescript
from pyomni.core.task_parsers import parse_task_block
from pyomni.models.task import Task

def list_tasks(project_path: str) -> List[Task]:
    if project_path.lower() == "inbox":
        script = build_task_query_applescript("every inbox task")
    else:
        resolver_script, project_var = resolve_project_applescript(project_path)
        selector = f"every task of {project_var}"
        script = f'''
tell application "OmniFocus"
    {resolver_script}
    tell default document
        {build_task_query_applescript("every task of currentProject")}
    end tell
end tell
'''

    output = run_applescript(script)
    print("======== RAW OUTPUT BEGIN ========")
    print(output)
    print("======== RAW OUTPUT END ==========")

    if not output.strip():
        return []

    blocks = output.strip().split("\n\n")
    return [parse_task_block(block) for block in blocks if block.strip()]

# # src/pyomni/core/task_ops.py

# from typing import List
# from pyomni.core.applescript import run_applescript
# from pyomni.core.resolvers import resolve_project_applescript
# from pyomni.models.task import Task

# def list_tasks(project_path: str) -> List[Task]:
#     if project_path.lower() == "inbox":
#         script = """
# tell application "OmniFocus"
#     tell default document
#         set props to {}
#         repeat with t in every inbox task
#             set end of props to (id of t as text) & "\t" & (name of t)
#         end repeat
#         return props
#     end tell
# end tell
# """
#     else:
#         resolver_script, project_var = resolve_project_applescript(project_path)
#         script = f"""
# tell application "OmniFocus"
#     {resolver_script}
#     tell default document
#         set props to {{}}
#         repeat with t in every task of {project_var}
#             set end of props to (id of t as text) & "\t" & (name of t)
#         end repeat
#         return props
#     end tell
# end tell
# """

#     output = run_applescript(script)

#     print("RAW APPLESCRIPT OUTPUT:")
#     print(output)

#     if not output:
#         return []

#     task_blocks = output.strip().split("\n\n")
#     return [parse_task_block(block) for block in task_blocks if block.strip()]


def create_task(name: str, project_path: Optional[str] = None, note: Optional[str] = None, flagged: bool = False):
    if not name:
        raise ValueError("Task name is required")

    note_line = f'set note of newTask to "{note}"' if note else ""
    flagged_line = 'set flagged of newTask to true' if flagged else ""

    if project_path:
        resolver_script, project_var = resolve_project_applescript(project_path)
        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            tell default document
                set newTask to make new task with properties {{name: "{name}"}} at end of tasks of {project_var}
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

from typing import List, Optional
from pyomni.core.applescript import run_applescript
from pyomni.core.resolvers import resolve_project_applescript
from pyomni.core.resolvers import safe_resolve_project_applescript
from pyomni.core.task_scripts import build_task_query_applescript
from pyomni.core.task_parsers import parse_task_block
from pyomni.models.task import Task


def list_tasks(project_path: str) -> List[Task]:
    if project_path.lower() == "inbox":
        script = build_task_query_applescript("every inbox task")
    else:
        # resolver_script, project_var = resolve_project_applescript(project_path)
        resolver_script, project_var = safe_resolve_project_applescript(project_path)
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
    # print("======== RAW OUTPUT BEGIN ========")
    # print(output)
    # print("======== RAW OUTPUT END ==========")

    if not output.strip():
        return []

    blocks = output.strip().split("\n\n")
    return [parse_task_block(block) for block in blocks if block.strip()]



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


def is_inbox_task(task_id: str) -> bool:
    """Check if a task is in the Inbox."""
    script = f'''
    tell application "OmniFocus"
        tell default document
            return exists (first inbox task whose id is "{task_id}")
        end tell
    end tell
    '''
    return run_applescript(script).strip().lower() == "true"

def complete_task(task_id: str):
    """
    Marks a task as completed in OmniFocus.

    - For regular tasks, it marks them as completed directly.
    - For inbox tasks (which cannot be completed directly via AppleScript),
    it moves them into a special project called 'CompletedInboxTasks',
    marks the task as complete, and then re-completes the project (if needed).

    Note:
    OmniFocus does not allow AppleScript to mark a project as 'completed' or 'dropped'.
    As a workaround, inbox tasks are moved to a project called 'CompletedInboxTasks' and marked complete.

    Warning: The project itself will remain active and visible unless manually completed or dropped in the OmniFocus UI.
    You may also hide this project by placing it in an archived or dropped folder.

    Alternatively, avoid scripting inbox task completion.
    """
    if is_inbox_task(task_id):
        # Ensure the target project exists
        setup_script = '''
        tell application "OmniFocus"
            tell default document
                if not (exists (first flattened project whose name is "CompletedInboxTasks")) then
                    make new project with properties {name: "CompletedInboxTasks"}
                end if
            end tell
        end tell
        '''
        run_applescript(setup_script)

        # Move the inbox task, mark it complete, and re-complete the container project
        script = f'''
        tell application "OmniFocus"
            tell default document
                set inboxTask to first inbox task whose id is "{task_id}"
                set destProject to first flattened project whose name is "CompletedInboxTasks"
                move inboxTask to end of tasks of destProject
                mark complete inboxTask
            end tell
        end tell
        '''
    else:
        # Normal task completion
        script = f'''
        tell application "OmniFocus"
            tell default document
                set t to first flattened task whose id is "{task_id}"
                mark complete t
            end tell
        end tell
        '''
    
    run_applescript(script)
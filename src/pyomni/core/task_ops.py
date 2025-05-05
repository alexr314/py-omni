from pyomni.core.applescript import run_applescript
from pyomni.core.resolvers import resolve_project_applescript

def list_tasks(project_path: str) -> list[str]:
    if project_path.lower() == "inbox":
        script = '''
        tell application "OmniFocus"
            tell default document
                get name of every inbox task
            end tell
        end tell
        '''
    else:
        resolver_script, project_var = resolve_project_applescript(project_path)
        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            tell {project_var}
                get name of every task
            end tell
        end tell
        '''
    output = run_applescript(script)
    return [t.strip() for t in output.split(", ")] if output else []


def create_task(name: str, project_path: str = None, note: str = None, flagged: bool = False):
    if not name:
        raise ValueError("Task name is required")

    note_line = f'set note of newTask to "{note}"' if note else ''
    flagged_line = 'set flagged of newTask to true' if flagged else ''

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

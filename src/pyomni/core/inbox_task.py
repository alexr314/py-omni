from pyomni.core.applescript import run_applescript

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
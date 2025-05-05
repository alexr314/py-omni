from pyomni.core.applescript import run_applescript
from pyomni.core.resolvers import resolve_folder_applescript

def list_projects_in_folder(folder_path: str) -> list[str]:
    resolver_script, folder_var = resolve_folder_applescript(folder_path)
    script = f'''
    tell application "OmniFocus"
        {resolver_script}
        tell {folder_var}
            get name of every project
        end tell
    end tell
    '''
    output = run_applescript(script)
    return [p.strip() for p in output.split(", ")] if output else []

def list_subfolders(folder_path: str) -> list[str]:
    resolver_script, folder_var = resolve_folder_applescript(folder_path)
    script = f'''
    tell application "OmniFocus"
        {resolver_script}
        tell {folder_var}
            get name of every folder
        end tell
    end tell
    '''
    output = run_applescript(script)
    return [f.strip() for f in output.split(", ")] if output else []

def list_folders() -> list[str]:
    script = '''
    tell application "OmniFocus"
        tell default document
            get name of every folder
        end tell
    end tell
    '''
    output = run_applescript(script)
    return [f.strip() for f in output.split(", ")] if output else []

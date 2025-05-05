import subprocess
from pyomni.exceptions import (
    FolderNotFoundError,
    ProjectNotFoundError,
    AppleScriptExecutionError,
)

def run_applescript(script: str) -> str:
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        error_message = result.stderr.strip()
        if "Invalid index" in error_message and "folder" in error_message:
            raise FolderNotFoundError("Folder not found. Check the folder path.")
        elif "Invalid index" in error_message and "project" in error_message:
            raise ProjectNotFoundError("Project not found. Check the project name.")
        else:
            raise AppleScriptExecutionError(f"AppleScript error: {error_message}")
    return result.stdout.strip()

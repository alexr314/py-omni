# src/pyomni/client.py

import subprocess
from pyomni.exceptions import (
    OmniFocusError,
    FolderNotFoundError,
    ProjectNotFoundError,
    TaskNotFoundError,
    AppleScriptExecutionError,
)

class OmniFocusClient:
    def run_applescript(self, script: str) -> str:
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
    
    def _resolve_project_applescript(self, project_path: str) -> tuple[str, str]:
        """
        Resolves a nested project path like 'Folder > Subfolder > ProjectName'
        Returns:
            AppleScript lines to set a variable to the project reference
            Name of the project variable (always 'currentProject')
        """
        parts = [p.strip() for p in project_path.split(">")]
        folder_parts = parts[:-1]
        project_name = parts[-1]

        script_lines = ["set currentFolder to default document"]
        for folder in folder_parts:
            script_lines.append(
                f'set currentFolder to first folder of currentFolder whose name is "{folder}"'
            )
        script_lines.append(
            f'set currentProject to first project of currentFolder whose name is "{project_name}"'
        )
        return "\n".join(script_lines), "currentProject"


    def _resolve_folder_applescript(self, folder_path: str) -> tuple[str, str]:
        """
        Returns AppleScript to walk through a folder path like 'Work > Clients'
        Returns:
            resolver_script (str): Script to resolve the nested folder
            folder_var (str): The variable ('currentFolder') to refer to it
        """
        components = [f'"{part.strip()}"' for part in folder_path.split(">")]
        script_lines = ["set currentFolder to default document"]
        for name in components:
            script_lines.append(
                f'set currentFolder to first folder of currentFolder whose name is {name}'
            )
        return "\n".join(script_lines), "currentFolder"

    def list_projects_in_folder(self, folder_path: str) -> list[str]:
        resolver_script, folder_var = self._resolve_folder_applescript(folder_path)
        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            tell {folder_var}
                get name of every project
            end tell
        end tell
        '''
        output = self.run_applescript(script)
        return [p.strip() for p in output.split(", ")] if output else []

    def list_subfolders(self, folder_path: str) -> list[str]:
        resolver_script, folder_var = self._resolve_folder_applescript(folder_path)
        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            tell {folder_var}
                get name of every folder
            end tell
        end tell
        '''
        output = self.run_applescript(script)
        return [f.strip() for f in output.split(", ")] if output else []
    
    def list_folders(self) -> list[str]:
        script = '''
        tell application "OmniFocus"
            tell default document
                get name of every folder
            end tell
        end tell
        '''
        output = self.run_applescript(script)
        return [f.strip() for f in output.split(", ")] if output else []

    def list_tasks(self, project_path: str) -> list[str]:
        resolver_script, project_var = self._resolve_project_applescript(project_path)
        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            tell {project_var}
                get name of every task
            end tell
        end tell
        '''
        output = self.run_applescript(script)
        return [t.strip() for t in output.split(", ")] if output else []
    

    def create_task(self, name: str, project_path: str = None, note: str = None, flagged: bool = False):
        if not name:
            raise ValueError("Task name is required")

        if project_path:
            resolver_script, target_var = self._resolve_project_applescript(project_path)
            container_line = f'set theContainer to {target_var}'
        else:
            resolver_script = ''
            container_line = 'set theContainer to inbox of default document'

        note_line = f'set note of newTask to "{note}"' if note else ''
        flagged_line = 'set flagged of newTask to true' if flagged else ''

        script = f'''
        tell application "OmniFocus"
            {resolver_script}
            {container_line}
            tell theContainer
                set newTask to make new task with properties {{name: "{name}"}}
                {note_line}
                {flagged_line}
            end tell
        end tell
        '''

        self.run_applescript(script)

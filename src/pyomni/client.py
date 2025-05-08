from pyomni.core.task_ops import (
    list_tasks,
    create_task,
    complete_task
)
from pyomni.core.folder_ops import (
    list_folders,
    list_subfolders,
    list_projects_in_folder,
)

class OmniFocusClient:
    def list_tasks(self, project_path: str) -> list[str]:
        return list_tasks(project_path)

    def create_task(self, name, project_path=None, note=None, flagged=False):
        return create_task(name, project_path, note, flagged)

    def list_folders(self) -> list[str]:
        return list_folders()

    def list_subfolders(self, folder_path: str) -> list[str]:
        return list_subfolders(folder_path)

    def list_projects_in_folder(self, folder_path: str) -> list[str]:
        return list_projects_in_folder(folder_path)
    
    def complete_task(self, task_id: str):
        return complete_task(task_id)


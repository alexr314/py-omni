from pyomni.client import OmniFocusClient
from pyomni.core import list_tasks  # low-level function
from pyomni.models.task import Task     # dataclass
import pytest

def test_list_tasks_in_real_project():
    client = OmniFocusClient()
    tasks = client.list_tasks("API > Jobs")  # Replace with an actual project path
    assert isinstance(tasks, list)
    assert all(hasattr(t, "name") for t in tasks)  # safer than assuming str

def test_list_tasks_in_invalid_project_raises():
    client = OmniFocusClient()
    with pytest.raises(Exception):  # Ideally catch ProjectNotFoundError
        client.list_tasks("Nonexistent > GarbageProject")

def test_list_tasks_returns_objects():
    tasks = list_tasks("Inbox")
    assert all(isinstance(t, Task) for t in tasks)
    assert all(hasattr(t, "name") for t in tasks)

def test_task_metadata_fields_present():
    client = OmniFocusClient()
    tasks = client.list_tasks("Inbox")
    assert tasks, "Expected at least one task"
    task = tasks[0]
    assert isinstance(task, Task)
    assert task.id
    assert isinstance(task.completed, bool)
    assert isinstance(task.flagged, bool)
    assert isinstance(task.in_inbox, bool)
    assert hasattr(task, "creation_date")
    assert hasattr(task, "due_date")
    assert hasattr(task, "tags")

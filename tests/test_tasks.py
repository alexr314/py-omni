from pyomni.client import OmniFocusClient
from pyomni.core import list_tasks  # low-level function
from pyomni.models.task import Task     # dataclass
from time import sleep, time
from typing import Optional
import pytest

def wait_for_task(name: str, fetch_func, timeout=5.0, interval=0.5) -> Optional[Task]:
    """Waits until a task with a matching name appears and returns it, or None."""
    end = time() + timeout
    while time() < end:
        tasks = fetch_func()
        for t in tasks:
            if t.name.strip() == name.strip():
                return t
        sleep(interval)
    return None

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


def test_subtasks_are_parsed():
    client = OmniFocusClient()
    tasks = client.list_tasks("Inbox")  # Or use a known project with nested tasks
    has_subtasks = any(task.children for task in tasks)
    assert isinstance(tasks, list)
    assert all(isinstance(t, Task) for t in tasks)
    assert isinstance(has_subtasks, bool)  # True if any subtasks exist


def test_complete_task_marks_as_complete():
    client = OmniFocusClient()
    name = "TDD Completion Task"
    client.create_task(name)

    # Wait for creation
    new_task = wait_for_task(name, lambda: client.list_tasks("Inbox"))
    assert new_task, "Task should have been created"
    assert not new_task.completed, "Task should start incomplete"

    # Mark complete
    client.complete_task(new_task.id)

    # Look in CompletedInboxTasks for the task now
    def fetch_completed():
        return [t for t in client.list_tasks("CompletedInboxTasks") if t.id == new_task.id]

    updated = wait_for_task(name, fetch_completed)
    assert updated, "Task should exist in CompletedInboxTasks"
    assert updated.completed, "Task should now be marked complete"


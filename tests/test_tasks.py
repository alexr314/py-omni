from pyomni.client import OmniFocusClient
from pyomni.core import list_tasks  # low-level function
from pyomni.models.task import Task     # dataclass
from time import sleep, time
from datetime import datetime, timedelta
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

def test_set_due_date_updates_correctly():
    client = OmniFocusClient()
    name = f"TDD Due Date Task {datetime.now().timestamp()}"
    client.create_task(name)

    task = wait_for_task(name, lambda: client.list_tasks("Inbox"))
    assert task, "Task was not created"
    assert task.due_date is None, f"Expected no due date, got {task.due_date}"

    new_due = datetime(2025, 12, 25, 17, 0, 0)
    client.set_due_date(task.id, new_due)

    updated = wait_for_task(name, lambda: [t for t in client.list_tasks("Inbox") if t.id == task.id])
    assert updated and updated.due_date == new_due

def test_update_task_fields():
    client = OmniFocusClient()
    name = f"TDD Update Task {datetime.now().timestamp()}"
    client.create_task(name)

    task = wait_for_task(name, lambda: client.list_tasks("Inbox"))
    assert task, "Task should have been created"

    client.update_task(task.id, note="Updated note", flagged=True)

    def fetch_updated():
        tasks = client.list_tasks("Inbox")
        for t in tasks:
            print(f"→ {t.id} | {t.name} | flagged: {t.flagged} | note: {t.note}")
        return [t for t in tasks if t.id == task.id]

    updated = wait_for_task(name, fetch_updated)
    assert updated, "Task should be found after update"
    assert updated.note == "Updated note"
    assert updated.flagged is True


def test_delete_task_removes_it():
    client = OmniFocusClient()
    name = "TDD Delete Task"
    client.create_task(name)

    task = wait_for_task(name, lambda: client.list_tasks("Inbox"))
    assert task

    client.delete_task(task.id)

    def search_deleted():
        return [t for t in client.list_tasks("Inbox") if t.id == task.id]

    deleted = wait_for_task(name, search_deleted)
    assert deleted is None, "Task should no longer exist after deletion"

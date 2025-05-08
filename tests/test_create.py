from pyomni.client import OmniFocusClient
from pyomni.models.task import Task
from time import sleep, time
from typing import Optional


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


def test_create_task_in_inbox_creates_task():
    client = OmniFocusClient()
    name = "TDD Inbox Task"

    # Snapshot before creation
    existing_ids = {t.id for t in client.list_tasks("Inbox") if t.name == name}

    client.create_task(name)

    def fetch_inbox_tasks():
        return [t for t in client.list_tasks("Inbox") if t.name == name and t.id not in existing_ids]

    new_task = wait_for_task(name, fetch_inbox_tasks)
    print("All task IDs for", name, ":", [(t.id, t.name) for t in client.list_tasks("Inbox")])
    assert new_task, f"Expected to find newly created task '{name}' in Inbox"


def test_create_task_in_project_creates_task():
    client = OmniFocusClient()
    name = "TDD Project Task"
    project_path = "API > Jobs"

    # Record existing task IDs with that name
    existing_ids = {t.id for t in client.list_tasks(project_path) if t.name == name}

    # Create a new task
    client.create_task(name, project_path=project_path)

    def fetch_project_tasks():
        return [t for t in client.list_tasks(project_path) if t.name == name and t.id not in existing_ids]

    new_task = wait_for_task(name, fetch_project_tasks)
    print("All task IDs for", name, ":", [(t.id, t.name) for t in client.list_tasks(project_path)])
    assert new_task, f"Expected to find newly created task '{name}' in project '{project_path}'"

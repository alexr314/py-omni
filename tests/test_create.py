from pyomni.client import OmniFocusClient
from pyomni.models.task import Task  # <- make sure Task is importable

def test_create_task_in_inbox_creates_task():
    client = OmniFocusClient()
    name = "TDD Inbox Task"
    client.create_task(name)
    tasks = client.list_tasks("Inbox")
    assert any(t.name == name for t in tasks)

def test_create_task_in_project_creates_task():
    client = OmniFocusClient()
    name = "TDD Project Task"
    project_path = "API > Jobs"
    client.create_task(name, project_path=project_path)
    tasks = client.list_tasks(project_path)
    assert any(t.name == name for t in tasks)

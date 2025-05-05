from pyomni.client import OmniFocusClient

# def test_create_task_in_inbox_creates_visible_task():
#     client = OmniFocusClient()
#     task_name = "Test Task - Inbox"
#     client.create_task(task_name)

#     # Now check that it shows up somewhere in the Inbox
#     inbox_tasks = client.list_tasks("Inbox")  # We'll handle this specially in code
#     assert task_name in inbox_tasks

def test_create_task_in_inbox_creates_task():
    client = OmniFocusClient()
    name = "TDD Inbox Task"
    client.create_task(name)
    tasks = client.list_tasks("Inbox")
    assert name in tasks

def test_create_task_in_project_creates_task():
    client = OmniFocusClient()
    name = "TDD Project Task"
    project_path = "API > Jobs"
    client.create_task(name, project_path=project_path)
    tasks = client.list_tasks(project_path)
    assert name in tasks

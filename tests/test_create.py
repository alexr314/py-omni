from pyomni.client import OmniFocusClient

def test_create_task_in_inbox_creates_visible_task():
    client = OmniFocusClient()
    task_name = "Test Task - Inbox"
    client.create_task(task_name)

    # Now check that it shows up somewhere in the Inbox
    inbox_tasks = client.list_tasks("Inbox")  # We'll handle this specially in code
    assert task_name in inbox_tasks

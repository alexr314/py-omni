from pyomni.client import OmniFocusClient
import pytest

def test_list_tasks_in_real_project():
    client = OmniFocusClient()
    tasks = client.list_tasks("API > Jobs")  # Replace with an actual project path
    assert isinstance(tasks, list)
    assert all(isinstance(t, str) for t in tasks)

def test_list_tasks_in_invalid_project_raises():
    client = OmniFocusClient()
    with pytest.raises(Exception):  # or ProjectNotFoundError
        client.list_tasks("Nonexistent > GarbageProject")

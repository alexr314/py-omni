from pyomni.client import OmniFocusClient

def test_list_projects_in_known_folder():
    client = OmniFocusClient()
    projects = client.list_projects_in_folder("API")  # Replace with a real one
    assert isinstance(projects, list)

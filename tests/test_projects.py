from pyomni.client import OmniFocusClient
import pytest

def test_list_projects_in_real_folder():
    client = OmniFocusClient()
    projects = client.list_projects_in_folder("API")  # replace with one that exists
    assert isinstance(projects, list)
    assert all(isinstance(p, str) for p in projects)

def test_list_projects_in_invalid_folder_raises():
    client = OmniFocusClient()
    with pytest.raises(Exception):  # You can use FolderNotFoundError if you want
        client.list_projects_in_folder("This Folder Does Not Exist")

from pyomni.client import OmniFocusClient
import pytest

def test_list_subfolders_in_real_folder():
    client = OmniFocusClient()
    subfolders = client.list_subfolders("API")  # replace with real folder
    assert isinstance(subfolders, list)
    assert all(isinstance(f, str) for f in subfolders)

def test_list_subfolders_in_invalid_folder_raises():
    client = OmniFocusClient()
    with pytest.raises(Exception):  # or FolderNotFoundError
        client.list_subfolders("Not a Real Folder")

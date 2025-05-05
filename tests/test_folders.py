from pyomni.client import OmniFocusClient

def test_list_top_level_folders_returns_names():
    client = OmniFocusClient()
    folders = client.list_folders()  # This doesn't exist yet
    assert isinstance(folders, list)
    assert all(isinstance(f, str) for f in folders)
    assert len(folders) > 0  # Adjust if your OmniFocus is empty

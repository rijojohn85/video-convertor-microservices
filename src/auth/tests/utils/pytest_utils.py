import pytest

def pytest_collection_modifyitems(items)->None:
    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
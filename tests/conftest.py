import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activity state after each test."""
    original_activities = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_activities))

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import main as main_module
from app.main import app


@pytest.fixture
def client():
    original_connect = main_module.connect_to_mongo
    original_close = main_module.close_mongo_connection

    async def fake_connect():
        return None

    async def fake_close():
        return None

    main_module.connect_to_mongo = fake_connect
    main_module.close_mongo_connection = fake_close

    with TestClient(app) as test_client:
        yield test_client

    main_module.connect_to_mongo = original_connect
    main_module.close_mongo_connection = original_close


def get_dependency(path, method):
    for route in app.routes:
        if route.path == path and method in route.methods:
            return route.dependant.dependencies[0].call
    return None


@pytest.fixture
def override_customer():
    dependency = get_dependency("/tickets", "POST")
    app.dependency_overrides[dependency] = lambda: {"id": "customer-1", "role": "customer"}
    dependency = get_dependency("/tickets/my", "GET")
    app.dependency_overrides[dependency] = lambda: {"id": "customer-1", "role": "customer"}
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_admin():
    paths = [
        ("/tickets", "GET"),
        ("/tickets/{ticket_id}/assign", "PUT"),
        ("/admin/reports", "GET"),
        ("/network", "GET"),
        ("/network/{network_id}", "GET"),
        ("/network", "POST"),
        ("/network/{network_id}", "PUT"),
    ]

    for path, method in paths:
        dependency = get_dependency(path, method)
        app.dependency_overrides[dependency] = lambda: {"id": "admin-1", "role": "admin"}

    yield
    app.dependency_overrides.clear()


@pytest.fixture
def override_engineer():
    dependency = get_dependency("/engineer/tickets", "GET")
    app.dependency_overrides[dependency] = lambda: {"id": "engineer-1", "role": "engineer"}
    yield
    app.dependency_overrides.clear()

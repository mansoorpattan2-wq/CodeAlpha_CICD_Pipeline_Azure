"""
test_app.py
-----------
Basic automated tests for the Flask app.
Run locally with:  pytest tests/
These same tests can later be wired into the Azure Pipeline as a "test stage"
before the Docker image is built (best practice: never ship untested code).
"""

import sys
import os

# Allow "import app" to find app/app.py when running pytest from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_home_page_loads(client):
    """The home page should return HTTP 200 and contain the app title."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"CodeAlpha" in response.data


def test_health_endpoint(client):
    """The health check endpoint should return status 'healthy'."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_info_endpoint(client):
    """The /api/info endpoint should return valid JSON with expected keys."""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.get_json()
    assert "app_name" in data
    assert "version" in data
    assert "environment" in data

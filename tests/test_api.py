"""Tests for the API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "F1 Fantasy Analysis API"
    assert data["status"] == "online"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


# Note: The following tests would require mocking the F1DataFetcher
# to avoid making actual API calls during testing.
# This is just a placeholder for demonstration purposes.

@pytest.mark.skip(reason="Requires mocking F1DataFetcher")
def test_get_races():
    """Test the get_races endpoint."""
    response = client.get("/api/v1/races")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.skip(reason="Requires mocking F1DataFetcher")
def test_get_drivers():
    """Test the get_drivers endpoint."""
    response = client.get("/api/v1/drivers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.skip(reason="Requires mocking F1DataFetcher")
def test_get_teams():
    """Test the get_teams endpoint."""
    response = client.get("/api/v1/teams")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.skip(reason="Requires mocking F1DataFetcher")
def test_get_driver_value_analysis():
    """Test the get_driver_value_analysis endpoint."""
    response = client.get("/api/v1/analysis/driver-value")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.skip(reason="Requires mocking F1DataFetcher")
def test_get_optimal_team():
    """Test the get_optimal_team endpoint."""
    response = client.get("/api/v1/analysis/optimal-team")
    assert response.status_code == 200
    data = response.json()
    assert "drivers" in data
    assert "team" in data
    assert "remaining_budget" in data 
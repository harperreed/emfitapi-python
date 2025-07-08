# ABOUTME: Test configuration and shared fixtures
# ABOUTME: Provides common test setup and utilities for the test suite

import logging
from unittest.mock import Mock

import pytest

from emfit.api import EmfitAPI


@pytest.fixture
def api_without_token():
    """Create EmfitAPI instance without token."""
    return EmfitAPI()


@pytest.fixture
def api_with_token():
    """Create EmfitAPI instance with test token."""
    return EmfitAPI(token="test_token_123")


@pytest.fixture
def sample_login_response():
    """Sample login response data."""
    return {"token": "sample_auth_token_456", "user_id": 123, "username": "testuser"}


@pytest.fixture
def sample_user_data():
    """Sample user data response."""
    return {
        "user_id": 123,
        "username": "testuser",
        "email": "testuser@example.com",
        "devices": [{"id": "device123", "name": "Bedroom", "model": "QS"}],
    }


@pytest.fixture
def sample_device_status():
    """Sample device status response."""
    return {
        "device_id": "device123",
        "status": "online",
        "last_seen": "2023-01-15T10:30:00Z",
        "battery_level": 95,
    }


@pytest.fixture
def sample_presence_data():
    """Sample presence data response."""
    return {
        "device_id": "device123",
        "presence_id": "presence456",
        "start_time": "2023-01-15T22:00:00Z",
        "end_time": "2023-01-16T06:30:00Z",
        "sleep_score": 85,
        "heart_rate_avg": 65,
        "respiratory_rate_avg": 16,
    }


@pytest.fixture
def sample_trends_data():
    """Sample trends data response."""
    return {
        "device_id": "device123",
        "start_date": "2023-01-01",
        "end_date": "2023-01-31",
        "trends": [
            {"date": "2023-01-01", "sleep_score": 80},
            {"date": "2023-01-02", "sleep_score": 85},
        ],
    }


@pytest.fixture
def mock_logger():
    """Mock logger for testing logging functionality."""
    return Mock(spec=logging.Logger)


@pytest.fixture
def disable_logging():
    """Disable logging during tests to reduce noise."""
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def capture_requests():
    """Fixture to capture and inspect HTTP requests."""
    captured_requests = []

    def capture_request(method, url, **kwargs):
        captured_requests.append({"method": method, "url": url, "kwargs": kwargs})

    return captured_requests, capture_request

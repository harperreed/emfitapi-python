# ABOUTME: Unit tests for the EmfitAPI class
# ABOUTME: Tests authentication, request handling, and all API methods with mocked responses

import logging
from unittest.mock import patch

import pytest
import responses

from emfit.api import EmfitAPI


class TestEmfitAPI:
    """Test suite for EmfitAPI class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.api = EmfitAPI()
        self.base_url = "https://qs-api.emfit.com/api/v1"
        self.test_token = "test_token_123"
        self.test_device_id = "test_device_123"

    def test_init_without_token(self):
        """Test EmfitAPI initialization without token."""
        api = EmfitAPI()
        assert api.base_url == self.base_url
        assert not hasattr(api, "token")
        assert isinstance(api.logger, logging.Logger)

    def test_init_with_token(self):
        """Test EmfitAPI initialization with token."""
        api = EmfitAPI(token=self.test_token)
        assert api.base_url == self.base_url
        assert api.token == self.test_token
        assert isinstance(api.logger, logging.Logger)

    @responses.activate
    def test_login_success(self):
        """Test successful login."""
        login_response = {
            "token": self.test_token,
            "remember_token": "remember_123",
            "user": {"id": 123, "username": "testuser", "email": "test@example.com"},
        }

        responses.add(
            responses.POST, f"{self.base_url}/login", json=login_response, status=200
        )

        result = self.api.login("testuser", "testpass")

        assert result == login_response
        assert self.api.token == self.test_token
        assert len(responses.calls) == 1
        assert responses.calls[0].request.body == "username=testuser&password=testpass"

    @responses.activate
    def test_login_failure(self):
        """Test failed login."""
        responses.add(
            responses.POST,
            f"{self.base_url}/login",
            json={"error": "Invalid credentials"},
            status=401,
        )

        with pytest.raises(Exception) as exc_info:
            self.api.login("testuser", "wrongpass")

        assert "Login failed with status code 401" in str(exc_info.value)
        assert not hasattr(self.api, "token")

    @responses.activate
    def test_handle_request_success(self):
        """Test successful request handling."""
        self.api.token = self.test_token
        test_response = {"data": "test_data"}

        responses.add(
            responses.GET, f"{self.base_url}/test", json=test_response, status=200
        )

        result = self.api.handle_request(f"{self.base_url}/test")

        assert result == test_response
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["Authorization"]
            == f"Bearer {self.test_token}"
        )

    @responses.activate
    def test_handle_request_failure(self):
        """Test failed request handling."""
        self.api.token = self.test_token

        responses.add(
            responses.GET,
            f"{self.base_url}/test",
            json={"error": "Not found"},
            status=404,
        )

        with pytest.raises(Exception) as exc_info:
            self.api.handle_request(f"{self.base_url}/test")

        assert "Request failed with status code 404" in str(exc_info.value)

    @responses.activate
    def test_handle_request_invalid_json(self):
        """Test request handling with invalid JSON response."""
        self.api.token = self.test_token

        responses.add(
            responses.GET, f"{self.base_url}/test", body="invalid json", status=200
        )

        with pytest.raises(ValueError):
            self.api.handle_request(f"{self.base_url}/test")

    @responses.activate
    def test_get_user(self):
        """Test get_user method."""
        self.api.token = self.test_token
        user_response = {
            "user": {"id": 123, "username": "testuser", "email": "test@example.com"}
        }

        responses.add(
            responses.GET, f"{self.base_url}/user/get", json=user_response, status=200
        )

        result = self.api.get_user()

        assert result == user_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_device_status(self):
        """Test get_device_status method."""
        self.api.token = self.test_token
        status_response = {
            "device_index": self.test_device_id,
            "description": "present",
            "from": 1730813827000,
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/device/status/{self.test_device_id}",
            json=status_response,
            status=200,
        )

        result = self.api.get_device_status(self.test_device_id)

        assert result == status_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_device_info(self):
        """Test get_device_info method."""
        self.api.token = self.test_token
        device_response = {
            "device_name": "Test Device",
            "firmware": "120.2.2.1",
            "field1": "left side",
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/device/{self.test_device_id}",
            json=device_response,
            status=200,
        )

        result = self.api.get_device_info(self.test_device_id)

        assert result == device_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_latest_presence(self):
        """Test get_latest_presence method."""
        self.api.token = self.test_token
        presence_response = {
            "id": "672a1f93d41d8c004324905d",
            "device_id": self.test_device_id,
            "sleep_duration": 27240,
            "sleep_efficiency": 83,
            "from_utc": "2024-11-05 04:22:00",
            "to_utc": "2024-11-05 13:37:00",
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/presence/{self.test_device_id}/latest",
            json=presence_response,
            status=200,
        )

        result = self.api.get_latest_presence(self.test_device_id)

        assert result == presence_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_presence(self):
        """Test get_presence method."""
        self.api.token = self.test_token
        presence_id = "672a1f93d41d8c004324905d"
        presence_response = {
            "id": presence_id,
            "device_id": self.test_device_id,
            "sleep_duration": 27240,
            "sleep_efficiency": 83,
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/presence/{self.test_device_id}/{presence_id}",
            json=presence_response,
            status=200,
        )

        result = self.api.get_presence(self.test_device_id, presence_id)

        assert result == presence_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_trends(self):
        """Test get_trends method."""
        self.api.token = self.test_token
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        trends_response = {
            "trends": [
                {"date": "2024-01-01", "sleep_score": 85},
                {"date": "2024-01-02", "sleep_score": 90},
            ]
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/trends/{self.test_device_id}/{start_date}/{end_date}",
            json=trends_response,
            status=200,
        )

        result = self.api.get_trends(self.test_device_id, start_date, end_date)

        assert result == trends_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_timeline(self):
        """Test get_timeline method."""
        self.api.token = self.test_token
        start_date = "2024-01-01"
        end_date = "2024-01-31"
        timeline_response = {
            "timeline": [
                {"timestamp": 1704067200, "event": "sleep_start"},
                {"timestamp": 1704096000, "event": "sleep_end"},
            ]
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/timeline/{self.test_device_id}/{start_date}/{end_date}",
            json=timeline_response,
            status=200,
        )

        result = self.api.get_timeline(self.test_device_id, start_date, end_date)

        assert result == timeline_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_notification_settings(self):
        """Test get_notification_settings method."""
        self.api.token = self.test_token
        notification_response = {
            "device_id": self.test_device_id,
            "sms_alert": False,
            "email_alert": True,
            "alarm_profile": "gentle",
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/device/notification-settings/{self.test_device_id}",
            json=notification_response,
            status=200,
        )

        result = self.api.get_notification_settings(self.test_device_id)

        assert result == notification_response
        assert len(responses.calls) == 1

    def test_all_methods_use_handle_request(self):
        """Test that all API methods use the handle_request method."""
        self.api.token = self.test_token

        with patch.object(self.api, "handle_request") as mock_handle:
            mock_handle.return_value = {"test": "data"}

            # Test all methods that should use handle_request
            methods_to_test = [
                (self.api.get_user, []),
                (self.api.get_device_status, [self.test_device_id]),
                (self.api.get_device_info, [self.test_device_id]),
                (self.api.get_latest_presence, [self.test_device_id]),
                (self.api.get_presence, [self.test_device_id, "presence_id"]),
                (
                    self.api.get_trends,
                    [self.test_device_id, "2024-01-01", "2024-01-31"],
                ),
                (
                    self.api.get_timeline,
                    [self.test_device_id, "2024-01-01", "2024-01-31"],
                ),
                (self.api.get_notification_settings, [self.test_device_id]),
            ]

            for method, args in methods_to_test:
                result = method(*args)
                assert result == {"test": "data"}

            # Verify handle_request was called the expected number of times
            assert mock_handle.call_count == len(methods_to_test)

    def test_logging_configuration(self):
        """Test that logging is properly configured."""
        api = EmfitAPI()
        assert api.logger.name == "emfit.api"
        assert isinstance(api.logger, logging.Logger)

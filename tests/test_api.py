# ABOUTME: Comprehensive test suite for EmfitAPI class
# ABOUTME: Tests authentication, request handling, endpoints, and error scenarios

import json
import logging
from unittest.mock import patch

import pytest
import requests
import responses

from emfit.api import EmfitAPI


class TestEmfitAPIInitialization:
    """Test EmfitAPI class initialization and basic properties."""

    def test_init_without_token(self):
        """Test EmfitAPI initialization without token."""
        api = EmfitAPI()
        assert api.base_url == "https://qs-api.emfit.com/api/v1"
        assert not hasattr(api, "token")
        assert isinstance(api.logger, logging.Logger)

    def test_init_with_token(self):
        """Test EmfitAPI initialization with token."""
        token = "test_token_123"
        api = EmfitAPI(token=token)
        assert api.base_url == "https://qs-api.emfit.com/api/v1"
        assert api.token == token
        assert isinstance(api.logger, logging.Logger)

    def test_base_url_is_correct(self):
        """Test that base URL is set correctly."""
        api = EmfitAPI()
        assert api.base_url == "https://qs-api.emfit.com/api/v1"

    def test_logger_initialization(self):
        """Test that logger is initialized properly."""
        api = EmfitAPI()
        assert api.logger.name == "emfit.api"


class TestEmfitAPIAuthentication:
    """Test authentication flow and token management."""

    @responses.activate
    def test_login_success(self):
        """Test successful login flow."""
        username = "testuser"
        password = "testpass"
        token = "auth_token_123"

        responses.add(
            responses.POST,
            "https://qs-api.emfit.com/api/v1/login",
            json={"token": token, "user_id": 123},
            status=200,
        )

        api = EmfitAPI()
        result = api.login(username, password)

        assert api.token == token
        assert result["token"] == token
        assert result["user_id"] == 123

    @responses.activate
    def test_login_failure(self):
        """Test login failure with invalid credentials."""
        username = "baduser"
        password = "badpass"

        responses.add(
            responses.POST,
            "https://qs-api.emfit.com/api/v1/login",
            json={"error": "Invalid credentials"},
            status=401,
        )

        api = EmfitAPI()
        with pytest.raises(Exception) as exc_info:
            api.login(username, password)

        assert "Login failed with status code 401" in str(exc_info.value)
        assert not hasattr(api, "token")

    @responses.activate
    def test_token_persistence(self):
        """Test that token is stored correctly after login."""
        username = "testuser"
        password = "testpass"
        token = "persistent_token_456"

        responses.add(
            responses.POST,
            "https://qs-api.emfit.com/api/v1/login",
            json={"token": token},
            status=200,
        )

        api = EmfitAPI()
        api.login(username, password)

        assert api.token == token
        # Token should persist for subsequent requests
        assert api.token == token


class TestEmfitAPIRequestHandling:
    """Test the central request handling method."""

    @responses.activate
    def test_handle_request_success(self):
        """Test successful request handling."""
        api = EmfitAPI(token="test_token")
        test_url = "https://qs-api.emfit.com/api/v1/test"
        response_data = {"data": "test_response"}

        responses.add(responses.GET, test_url, json=response_data, status=200)

        result = api.handle_request(test_url)

        assert result == response_data
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["Authorization"] == "Bearer test_token"
        )

    @responses.activate
    def test_handle_request_error(self):
        """Test error handling for non-200 status codes."""
        api = EmfitAPI(token="test_token")
        test_url = "https://qs-api.emfit.com/api/v1/test"

        responses.add(responses.GET, test_url, json={"error": "Not found"}, status=404)

        with pytest.raises(Exception) as exc_info:
            api.handle_request(test_url)

        assert "Request failed with status code 404" in str(exc_info.value)

    @responses.activate
    def test_handle_request_json_error(self):
        """Test handling of invalid JSON responses."""
        api = EmfitAPI(token="test_token")
        test_url = "https://qs-api.emfit.com/api/v1/test"

        responses.add(responses.GET, test_url, body="invalid json", status=200)

        with pytest.raises(json.JSONDecodeError):
            api.handle_request(test_url)

    @responses.activate
    def test_handle_request_post_method(self):
        """Test handle_request with POST method."""
        api = EmfitAPI(token="test_token")
        test_url = "https://qs-api.emfit.com/api/v1/test"
        response_data = {"success": True}

        responses.add(responses.POST, test_url, json=response_data, status=200)

        result = api.handle_request(test_url, method="post", data={"key": "value"})

        assert result == response_data
        assert len(responses.calls) == 1
        assert (
            responses.calls[0].request.headers["Authorization"] == "Bearer test_token"
        )


class TestEmfitAPIEndpoints:
    """Test all GET endpoint methods."""

    @pytest.fixture
    def api(self):
        """Create EmfitAPI instance with test token."""
        return EmfitAPI(token="test_token")

    @responses.activate
    def test_get_user(self, api):
        """Test get_user endpoint."""
        response_data = {"user_id": 123, "username": "testuser"}
        responses.add(
            responses.GET,
            "https://qs-api.emfit.com/api/v1/user/get",
            json=response_data,
            status=200,
        )

        result = api.get_user()
        assert result == response_data

    @responses.activate
    def test_get_device_status(self, api):
        """Test get_device_status endpoint."""
        device_id = "device123"
        response_data = {"device_id": device_id, "status": "online"}
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/device/status/{device_id}",
            json=response_data,
            status=200,
        )

        result = api.get_device_status(device_id)
        assert result == response_data

    @responses.activate
    def test_get_device_info(self, api):
        """Test get_device_info endpoint."""
        device_id = "device123"
        response_data = {"device_id": device_id, "model": "QS", "version": "1.0"}
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/device/{device_id}",
            json=response_data,
            status=200,
        )

        result = api.get_device_info(device_id)
        assert result == response_data

    @responses.activate
    def test_get_latest_presence(self, api):
        """Test get_latest_presence endpoint."""
        device_id = "device123"
        response_data = {"device_id": device_id, "presence": "in_bed"}
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/presence/{device_id}/latest",
            json=response_data,
            status=200,
        )

        result = api.get_latest_presence(device_id)
        assert result == response_data

    @responses.activate
    def test_get_presence(self, api):
        """Test get_presence endpoint."""
        device_id = "device123"
        presence_id = "presence456"
        response_data = {"device_id": device_id, "presence_id": presence_id}
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/presence/{device_id}/{presence_id}",
            json=response_data,
            status=200,
        )

        result = api.get_presence(device_id, presence_id)
        assert result == response_data

    @responses.activate
    def test_get_trends(self, api):
        """Test get_trends endpoint."""
        device_id = "device123"
        start_date = "2023-01-01"
        end_date = "2023-01-31"
        response_data = {"device_id": device_id, "trends": []}
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/trends/{device_id}/{start_date}/{end_date}",
            json=response_data,
            status=200,
        )

        result = api.get_trends(device_id, start_date, end_date)
        assert result == response_data

    @responses.activate
    def test_get_timeline(self, api):
        """Test get_timeline endpoint."""
        device_id = "device123"
        start_date = "2023-01-01"
        end_date = "2023-01-31"
        response_data = {"device_id": device_id, "timeline": []}
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/timeline/{device_id}/{start_date}/{end_date}",
            json=response_data,
            status=200,
        )

        result = api.get_timeline(device_id, start_date, end_date)
        assert result == response_data

    @responses.activate
    def test_get_notification_settings(self, api):
        """Test get_notification_settings endpoint."""
        device_id = "device123"
        response_data = {"device_id": device_id, "notifications": True}
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/device/notification-settings/{device_id}",
            json=response_data,
            status=200,
        )

        result = api.get_notification_settings(device_id)
        assert result == response_data


class TestEmfitAPIEdgeCases:
    """Test edge cases and error scenarios."""

    def test_empty_token_handling(self):
        """Test behavior with empty token."""
        api = EmfitAPI()
        # Should not have token attribute
        assert not hasattr(api, "token")

    def test_handle_request_without_token(self):
        """Test request handling without token."""
        api = EmfitAPI()
        with pytest.raises(AttributeError):
            api.handle_request("https://example.com")

    @responses.activate
    def test_invalid_device_id_handling(self):
        """Test handling of invalid device ID."""
        api = EmfitAPI(token="test_token")
        device_id = "invalid_device"

        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/device/status/{device_id}",
            json={"error": "Device not found"},
            status=404,
        )

        with pytest.raises(Exception) as exc_info:
            api.get_device_status(device_id)

        assert "Request failed with status code 404" in str(exc_info.value)

    @responses.activate
    def test_network_failure_scenario(self):
        """Test network failure handling."""
        api = EmfitAPI(token="test_token")

        responses.add(
            responses.GET,
            "https://qs-api.emfit.com/api/v1/user/get",
            body=requests.exceptions.ConnectionError("Network error"),
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            api.get_user()

    @responses.activate
    def test_timeout_handling(self):
        """Test timeout handling."""
        api = EmfitAPI(token="test_token")

        responses.add(
            responses.GET,
            "https://qs-api.emfit.com/api/v1/user/get",
            body=requests.exceptions.Timeout("Request timed out"),
        )

        with pytest.raises(requests.exceptions.Timeout):
            api.get_user()


class TestEmfitAPIURLConstruction:
    """Test URL construction for different endpoints."""

    @pytest.fixture
    def api(self):
        """Create EmfitAPI instance."""
        return EmfitAPI(token="test_token")

    def test_login_url_construction(self, api):
        """Test login URL construction."""
        expected_url = "https://qs-api.emfit.com/api/v1/login"
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"token": "test"}
            try:
                api.login("user", "pass")
            except Exception:
                pass
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            assert args[0] == expected_url

    def test_user_url_construction(self, api):
        """Test user endpoint URL construction."""
        expected_url = "https://qs-api.emfit.com/api/v1/user/get"
        with patch.object(api, "handle_request") as mock_handle:
            api.get_user()
            mock_handle.assert_called_once_with(expected_url)

    def test_device_status_url_construction(self, api):
        """Test device status URL construction."""
        device_id = "device123"
        expected_url = f"https://qs-api.emfit.com/api/v1/device/status/{device_id}"
        with patch.object(api, "handle_request") as mock_handle:
            api.get_device_status(device_id)
            mock_handle.assert_called_once_with(expected_url)

    def test_url_with_special_characters(self, api):
        """Test URL construction with special characters."""
        device_id = "device-123_test"
        expected_url = f"https://qs-api.emfit.com/api/v1/device/status/{device_id}"
        with patch.object(api, "handle_request") as mock_handle:
            api.get_device_status(device_id)
            mock_handle.assert_called_once_with(expected_url)


class TestEmfitAPIParameterValidation:
    """Test parameter validation for API methods."""

    @pytest.fixture
    def api(self):
        """Create EmfitAPI instance."""
        return EmfitAPI(token="test_token")

    def test_device_id_parameter_types(self, api):
        """Test device_id parameter with different types."""
        with patch.object(api, "handle_request") as mock_handle:
            # String device ID (normal case)
            api.get_device_status("device123")
            mock_handle.assert_called_with(
                "https://qs-api.emfit.com/api/v1/device/status/device123"
            )

            # Numeric device ID
            api.get_device_status(123)
            mock_handle.assert_called_with(
                "https://qs-api.emfit.com/api/v1/device/status/123"
            )

    def test_date_parameter_types(self, api):
        """Test date parameters with different formats."""
        device_id = "device123"
        with patch.object(api, "handle_request") as mock_handle:
            # String dates
            api.get_trends(device_id, "2023-01-01", "2023-01-31")
            expected_url = f"https://qs-api.emfit.com/api/v1/trends/{device_id}/2023-01-01/2023-01-31"
            mock_handle.assert_called_with(expected_url)

    def test_kwargs_parameter_passing(self, api):
        """Test that kwargs are passed correctly to handle_request."""
        with patch.object(api, "handle_request") as mock_handle:
            test_kwargs = {"param1": "value1", "param2": "value2"}
            api.get_user(**test_kwargs)
            mock_handle.assert_called_with(
                "https://qs-api.emfit.com/api/v1/user/get", **test_kwargs
            )


class TestEmfitAPILogging:
    """Test logging functionality."""

    @pytest.fixture
    def api(self):
        """Create EmfitAPI instance."""
        return EmfitAPI(token="test_token")

    def test_login_logging(self, api, caplog):
        """Test logging during login."""
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"token": "test"}

            with caplog.at_level(logging.INFO):
                api.login("testuser", "testpass")

            assert "Attempting to login user: testuser" in caplog.text
            assert "User testuser logged in successfully" in caplog.text

    def test_login_error_logging(self, api, caplog):
        """Test error logging during failed login."""
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 401

            with caplog.at_level(logging.ERROR):
                try:
                    api.login("baduser", "badpass")
                except Exception:
                    pass

            assert "Login failed with status code 401 for user: baduser" in caplog.text

    def test_request_logging(self, api, caplog):
        """Test logging during requests."""
        test_url = "https://qs-api.emfit.com/api/v1/test"
        with patch("requests.request") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.json.return_value = {"data": "test"}

            with caplog.at_level(logging.INFO):
                api.handle_request(test_url)

            assert f"Sending GET request to {test_url}" in caplog.text
            assert (
                f"Request to {test_url} succeeded with status code 200" in caplog.text
            )

    def test_request_error_logging(self, api, caplog):
        """Test error logging during failed requests."""
        test_url = "https://qs-api.emfit.com/api/v1/test"
        with patch("requests.request") as mock_request:
            mock_request.return_value.status_code = 404

            with caplog.at_level(logging.ERROR):
                try:
                    api.handle_request(test_url)
                except Exception:
                    pass

            assert f"Request to {test_url} failed with status code 404" in caplog.text


class TestEmfitAPIIntegration:
    """Integration tests for complete workflows."""

    @responses.activate
    def test_complete_workflow(self):
        """Test complete workflow from login to data retrieval."""
        username = "testuser"
        password = "testpass"
        token = "integration_token"
        device_id = "device123"

        # Mock login
        responses.add(
            responses.POST,
            "https://qs-api.emfit.com/api/v1/login",
            json={"token": token, "user_id": 123},
            status=200,
        )

        # Mock user data
        responses.add(
            responses.GET,
            "https://qs-api.emfit.com/api/v1/user/get",
            json={"user_id": 123, "devices": [{"id": device_id}]},
            status=200,
        )

        # Mock device status
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/device/status/{device_id}",
            json={"device_id": device_id, "status": "online"},
            status=200,
        )

        # Mock latest presence
        responses.add(
            responses.GET,
            f"https://qs-api.emfit.com/api/v1/presence/{device_id}/latest",
            json={"device_id": device_id, "presence": "in_bed"},
            status=200,
        )

        # Execute complete workflow
        api = EmfitAPI()

        # Login
        login_result = api.login(username, password)
        assert login_result["token"] == token
        assert api.token == token

        # Get user data
        user_data = api.get_user()
        assert user_data["user_id"] == 123

        # Get device status
        device_status = api.get_device_status(device_id)
        assert device_status["status"] == "online"

        # Get latest presence
        presence = api.get_latest_presence(device_id)
        assert presence["presence"] == "in_bed"

        # Verify all requests were made
        assert len(responses.calls) == 4

    @pytest.mark.e2e
    def test_real_api_workflow(self):
        """End-to-end test with real API (requires credentials)."""
        # This test should only run when explicitly requested
        # and with proper credentials set up
        import os

        username = os.getenv("EMFIT_TEST_USERNAME")
        password = os.getenv("EMFIT_TEST_PASSWORD")

        if not username or not password:
            pytest.skip("Real API credentials not provided")

        api = EmfitAPI()

        # Test login
        login_result = api.login(username, password)
        assert "token" in login_result
        assert api.token is not None

        # Test user data retrieval
        user_data = api.get_user()
        assert "user_id" in user_data or "id" in user_data

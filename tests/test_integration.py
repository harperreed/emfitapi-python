# ABOUTME: Integration tests for EmfitAPI class
# ABOUTME: Tests API workflows and interactions between methods using mocked HTTP responses

from unittest.mock import patch

import pytest
import responses

from emfit.api import EmfitAPI


class TestEmfitAPIIntegration:
    """Integration tests for EmfitAPI workflows."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.api = EmfitAPI()
        self.base_url = "https://qs-api.emfit.com/api/v1"
        self.test_token = "integration_test_token"
        self.test_device_id = "4613"
        self.test_user_id = 5065

    @responses.activate
    def test_full_authentication_workflow(self):
        """Test complete authentication workflow from login to API calls."""
        login_response = {
            "token": self.test_token,
            "remember_token": "remember_123",
            "user": {
                "id": self.test_user_id,
                "username": "testuser",
                "email": "test@example.com",
                "devices": f"{self.test_device_id},4470",
            },
        }

        user_response = {
            "user": login_response["user"],
            "device_settings": [
                {
                    "device_id": self.test_device_id,
                    "device_name": "Test Device",
                    "enabled_hrv": True,
                }
            ],
        }

        responses.add(
            responses.POST, f"{self.base_url}/login", json=login_response, status=200
        )

        responses.add(
            responses.GET, f"{self.base_url}/user/get", json=user_response, status=200
        )

        # Step 1: Login
        login_result = self.api.login("testuser", "testpass")
        assert login_result == login_response
        assert self.api.token == self.test_token

        # Step 2: Get user info using the authenticated token
        user_info = self.api.get_user()
        assert user_info == user_response
        assert user_info["user"]["id"] == self.test_user_id

        # Verify token was used in the second request
        assert len(responses.calls) == 2
        assert (
            responses.calls[1].request.headers["Authorization"]
            == f"Bearer {self.test_token}"
        )

    @responses.activate
    def test_device_data_workflow(self):
        """Test workflow for getting device information and data."""
        self.api.token = self.test_token

        device_info_response = {
            "device_name": "Master Bedroom",
            "firmware": "120.2.2.1",
            "field1": "left side",
        }

        device_status_response = {
            "device_index": self.test_device_id,
            "description": "present",
            "from": 1730813827000,
        }

        latest_presence_response = {
            "id": "672a1f93d41d8c004324905d",
            "device_id": self.test_device_id,
            "sleep_duration": 27240,
            "sleep_efficiency": 83,
            "sleep_score": 84,
            "from_utc": "2024-11-05 04:22:00",
            "to_utc": "2024-11-05 13:37:00",
            "navigation_data": [
                {"id": "672a1f93d41d8c004324905d", "date": "2024-11-05"}
            ],
        }

        specific_presence_response = {
            "id": "672a1f93d41d8c004324905d",
            "device_id": self.test_device_id,
            "sleep_duration": 27240,
            "sleep_efficiency": 83,
            "measured_hr_avg": 54,
            "measured_rr_avg": 17,
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/device/{self.test_device_id}",
            json=device_info_response,
            status=200,
        )

        responses.add(
            responses.GET,
            f"{self.base_url}/device/status/{self.test_device_id}",
            json=device_status_response,
            status=200,
        )

        responses.add(
            responses.GET,
            f"{self.base_url}/presence/{self.test_device_id}/latest",
            json=latest_presence_response,
            status=200,
        )

        responses.add(
            responses.GET,
            f"{self.base_url}/presence/{self.test_device_id}/672a1f93d41d8c004324905d",
            json=specific_presence_response,
            status=200,
        )

        # Step 1: Get device info
        device_info = self.api.get_device_info(self.test_device_id)
        assert device_info["device_name"] == "Master Bedroom"

        # Step 2: Get device status
        device_status = self.api.get_device_status(self.test_device_id)
        assert device_status["description"] == "present"

        # Step 3: Get latest presence data
        latest_presence = self.api.get_latest_presence(self.test_device_id)
        assert latest_presence["sleep_duration"] == 27240

        # Step 4: Get specific presence data using ID from latest
        presence_id = latest_presence["navigation_data"][0]["id"]
        specific_presence = self.api.get_presence(self.test_device_id, presence_id)
        assert specific_presence["measured_hr_avg"] == 54

        # Verify all requests were made with proper authentication
        assert len(responses.calls) == 4
        for call in responses.calls:
            assert call.request.headers["Authorization"] == f"Bearer {self.test_token}"

    @responses.activate
    def test_historical_data_workflow(self):
        """Test workflow for getting historical trends and timeline data."""
        self.api.token = self.test_token
        start_date = "2024-01-01"
        end_date = "2024-01-07"

        trends_response = {
            "trends": [
                {"date": "2024-01-01", "sleep_score": 85, "sleep_duration": 25200},
                {"date": "2024-01-02", "sleep_score": 90, "sleep_duration": 27000},
                {"date": "2024-01-03", "sleep_score": 82, "sleep_duration": 24600},
            ]
        }

        timeline_response = {
            "timeline": [
                {
                    "timestamp": 1704067200,
                    "event": "sleep_start",
                    "device_id": self.test_device_id,
                },
                {
                    "timestamp": 1704092400,
                    "event": "sleep_end",
                    "device_id": self.test_device_id,
                },
                {
                    "timestamp": 1704153600,
                    "event": "sleep_start",
                    "device_id": self.test_device_id,
                },
            ]
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/trends/{self.test_device_id}/{start_date}/{end_date}",
            json=trends_response,
            status=200,
        )

        responses.add(
            responses.GET,
            f"{self.base_url}/timeline/{self.test_device_id}/{start_date}/{end_date}",
            json=timeline_response,
            status=200,
        )

        # Step 1: Get trends data
        trends = self.api.get_trends(self.test_device_id, start_date, end_date)
        assert len(trends["trends"]) == 3
        assert trends["trends"][0]["sleep_score"] == 85

        # Step 2: Get timeline data for the same period
        timeline = self.api.get_timeline(self.test_device_id, start_date, end_date)
        assert len(timeline["timeline"]) == 3
        assert timeline["timeline"][0]["event"] == "sleep_start"

        # Verify proper URL construction and authentication
        assert len(responses.calls) == 2
        assert f"/{start_date}/{end_date}" in responses.calls[0].request.url
        assert f"/{start_date}/{end_date}" in responses.calls[1].request.url

    @responses.activate
    def test_error_handling_workflow(self):
        """Test error handling across multiple API calls."""
        self.api.token = self.test_token

        # First call succeeds
        responses.add(
            responses.GET,
            f"{self.base_url}/user/get",
            json={"user": {"id": 123}},
            status=200,
        )

        # Second call fails
        responses.add(
            responses.GET,
            f"{self.base_url}/device/{self.test_device_id}",
            json={"error": "Device not found"},
            status=404,
        )

        # First call should succeed
        user_info = self.api.get_user()
        assert user_info["user"]["id"] == 123

        # Second call should raise an exception
        with pytest.raises(Exception) as exc_info:
            self.api.get_device_info(self.test_device_id)

        assert "Request failed with status code 404" in str(exc_info.value)

    @responses.activate
    def test_notification_settings_workflow(self):
        """Test notification settings retrieval workflow."""
        self.api.token = self.test_token

        notification_response = {
            "device_id": self.test_device_id,
            "sms_alert": False,
            "email_alert": True,
            "alarm_profile": "gentle",
            "morning_alarm": True,
            "morning_alarm_time": "07:00",
        }

        responses.add(
            responses.GET,
            f"{self.base_url}/device/notification-settings/{self.test_device_id}",
            json=notification_response,
            status=200,
        )

        settings = self.api.get_notification_settings(self.test_device_id)
        assert settings["device_id"] == self.test_device_id
        assert settings["email_alert"] is True
        assert settings["sms_alert"] is False
        assert settings["morning_alarm_time"] == "07:00"

    def test_request_kwargs_propagation(self):
        """Test that kwargs are properly passed through to handle_request."""
        self.api.token = self.test_token

        with patch.object(self.api, "handle_request") as mock_handle:
            mock_handle.return_value = {"test": "data"}

            # Test that custom kwargs are passed through
            result = self.api.get_user(timeout=30, allow_redirects=False)

            assert result == {"test": "data"}
            mock_handle.assert_called_once_with(
                f"{self.base_url}/user/get", timeout=30, allow_redirects=False
            )

    @responses.activate
    def test_json_response_handling(self):
        """Test handling of different JSON response formats."""
        self.api.token = self.test_token

        # Test empty response
        responses.add(responses.GET, f"{self.base_url}/user/get", json={}, status=200)

        result = self.api.get_user()
        assert result == {}

        # Test nested response
        responses.add(
            responses.GET,
            f"{self.base_url}/device/{self.test_device_id}",
            json={
                "device": {
                    "info": {
                        "name": "Test Device",
                        "settings": {"enabled": True, "sensitivity": "high"},
                    }
                }
            },
            status=200,
        )

        result = self.api.get_device_info(self.test_device_id)
        assert result["device"]["info"]["name"] == "Test Device"
        assert result["device"]["info"]["settings"]["enabled"] is True

# ABOUTME: End-to-end tests for EmfitAPI class
# ABOUTME: Tests actual API interactions with real endpoints (requires valid credentials)

import logging
import os

import pytest

from emfit.api import EmfitAPI


class TestEmfitAPIE2E:
    """End-to-end tests for EmfitAPI with real API interactions."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.api = EmfitAPI()
        self.username = os.getenv("EMFIT_USERNAME")
        self.password = os.getenv("EMFIT_PASSWORD")
        self.token = os.getenv("EMFIT_TOKEN")
        self.device_id = os.getenv("EMFIT_DEVICE_ID")

    @pytest.fixture
    def authenticated_api(self):
        """Fixture providing an authenticated API instance."""
        api = EmfitAPI()

        if self.token:
            api.token = self.token
        elif self.username and self.password:
            api.login(self.username, self.password)
        else:
            pytest.skip("No authentication credentials provided")

        return api

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_USERNAME") and not os.getenv("EMFIT_TOKEN"),
        reason="No authentication credentials provided",
    )
    def test_login_with_credentials(self):
        """Test login with real credentials."""
        if not self.username or not self.password:
            pytest.skip("Username and password required for login test")

        api = EmfitAPI()

        # Test login
        response = api.login(self.username, self.password)

        # Verify response structure
        assert "token" in response
        assert "user" in response
        assert api.token == response["token"]
        assert isinstance(response["user"], dict)
        assert "id" in response["user"]
        assert "email" in response["user"]

    @pytest.mark.e2e
    def test_get_user_real_api(self, authenticated_api):
        """Test getting user information from real API."""
        user_info = authenticated_api.get_user()

        # Verify response structure
        assert "user" in user_info
        assert isinstance(user_info["user"], dict)
        assert "id" in user_info["user"]
        assert "email" in user_info["user"]
        assert "devices" in user_info["user"]

        # Verify notification settings are included
        if "notification_settings" in user_info:
            assert isinstance(user_info["notification_settings"], dict)

        # Verify device settings are included
        if "device_settings" in user_info:
            assert isinstance(user_info["device_settings"], list)

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_DEVICE_ID"), reason="Device ID required for device tests"
    )
    def test_get_device_info_real_api(self, authenticated_api):
        """Test getting device information from real API."""
        device_info = authenticated_api.get_device_info(self.device_id)

        # Verify response structure
        assert isinstance(device_info, dict)
        assert "device_name" in device_info
        assert "firmware" in device_info

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_DEVICE_ID"), reason="Device ID required for device tests"
    )
    def test_get_device_status_real_api(self, authenticated_api):
        """Test getting device status from real API."""
        device_status = authenticated_api.get_device_status(self.device_id)

        # Verify response structure
        assert isinstance(device_status, dict)
        assert "device_index" in device_status
        assert "description" in device_status
        assert device_status["description"] in ["present", "absent"]

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_DEVICE_ID"), reason="Device ID required for presence tests"
    )
    def test_get_latest_presence_real_api(self, authenticated_api):
        """Test getting latest presence data from real API."""
        latest_presence = authenticated_api.get_latest_presence(self.device_id)

        # Verify response structure
        assert isinstance(latest_presence, dict)
        assert "id" in latest_presence
        assert "device_id" in latest_presence
        assert "sleep_duration" in latest_presence
        assert "from_utc" in latest_presence
        assert "to_utc" in latest_presence

        # Verify sleep metrics are present
        sleep_metrics = [
            "sleep_efficiency",
            "sleep_score",
            "sleep_class_awake_duration",
            "sleep_class_deep_duration",
            "sleep_class_light_duration",
            "sleep_class_rem_duration",
        ]

        for metric in sleep_metrics:
            if metric in latest_presence:
                assert isinstance(latest_presence[metric], int | float)

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_DEVICE_ID"), reason="Device ID required for presence tests"
    )
    def test_get_specific_presence_real_api(self, authenticated_api):
        """Test getting specific presence data from real API."""
        # First get latest presence to get a valid presence ID
        latest_presence = authenticated_api.get_latest_presence(self.device_id)
        presence_id = latest_presence["id"]

        # Now get specific presence data
        specific_presence = authenticated_api.get_presence(self.device_id, presence_id)

        # Verify response structure
        assert isinstance(specific_presence, dict)
        assert specific_presence["id"] == presence_id
        assert specific_presence["device_id"] == self.device_id
        assert "sleep_duration" in specific_presence

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_DEVICE_ID"), reason="Device ID required for trends tests"
    )
    def test_get_trends_real_api(self, authenticated_api):
        """Test getting trends data from real API."""
        start_date = "2024-01-01"
        end_date = "2024-01-07"

        trends = authenticated_api.get_trends(self.device_id, start_date, end_date)

        # Verify response structure
        assert isinstance(trends, dict)
        # Note: Trends response structure may vary based on available data

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_DEVICE_ID"), reason="Device ID required for timeline tests"
    )
    def test_get_timeline_real_api(self, authenticated_api):
        """Test getting timeline data from real API."""
        start_date = "2024-01-01"
        end_date = "2024-01-07"

        timeline = authenticated_api.get_timeline(self.device_id, start_date, end_date)

        # Verify response structure
        assert isinstance(timeline, dict)
        # Note: Timeline response structure may vary based on available data

    @pytest.mark.e2e
    @pytest.mark.skipif(
        not os.getenv("EMFIT_DEVICE_ID"),
        reason="Device ID required for notification tests",
    )
    def test_get_notification_settings_real_api(self, authenticated_api):
        """Test getting notification settings from real API."""
        settings = authenticated_api.get_notification_settings(self.device_id)

        # Verify response structure
        assert isinstance(settings, dict)
        assert "device_id" in settings

        # Verify common notification settings
        expected_settings = [
            "sms_alert",
            "email_alert",
            "alarm_profile",
            "morning_alarm",
        ]

        for setting in expected_settings:
            if setting in settings:
                assert isinstance(settings[setting], bool | str)

    @pytest.mark.e2e
    def test_full_workflow_real_api(self, authenticated_api):
        """Test complete workflow with real API."""
        if not self.device_id:
            pytest.skip("Device ID required for full workflow test")

        # Step 1: Get user info
        user_info = authenticated_api.get_user()
        assert "user" in user_info

        # Step 2: Get device info
        device_info = authenticated_api.get_device_info(self.device_id)
        assert "device_name" in device_info

        # Step 3: Get device status
        device_status = authenticated_api.get_device_status(self.device_id)
        assert "description" in device_status

        # Step 4: Get latest presence
        latest_presence = authenticated_api.get_latest_presence(self.device_id)
        assert "sleep_duration" in latest_presence

        # Step 5: Get notification settings
        settings = authenticated_api.get_notification_settings(self.device_id)
        assert "device_id" in settings

    @pytest.mark.e2e
    def test_error_handling_real_api(self, authenticated_api):
        """Test error handling with real API."""
        # Test with invalid device ID
        invalid_device_id = "invalid_device_999999"

        with pytest.raises(Exception) as exc_info:
            authenticated_api.get_device_info(invalid_device_id)

        assert "Request failed with status code" in str(exc_info.value)

    @pytest.mark.e2e
    def test_logging_real_api(self, authenticated_api, caplog):
        """Test logging during real API interactions."""
        if not self.device_id:
            pytest.skip("Device ID required for logging test")

        with caplog.at_level(logging.INFO):
            authenticated_api.get_device_status(self.device_id)

        # Verify logging occurred
        assert any(
            "Retrieving device status" in record.message for record in caplog.records
        )
        assert any(
            "succeeded with status code" in record.message for record in caplog.records
        )

    @pytest.mark.e2e
    def test_request_timeout_real_api(self, authenticated_api):
        """Test request timeout handling with real API."""
        if not self.device_id:
            pytest.skip("Device ID required for timeout test")

        # Test with a very short timeout - this might fail due to network latency
        try:
            result = authenticated_api.get_device_status(self.device_id, timeout=0.001)
            # If it doesn't timeout, that's fine too
            assert isinstance(result, dict)
        except Exception as e:
            # Should be a timeout or connection error, not an API error
            assert "Request failed with status code" not in str(e)

    @pytest.mark.e2e
    def test_concurrent_requests_real_api(self, authenticated_api):
        """Test multiple concurrent requests to real API."""
        if not self.device_id:
            pytest.skip("Device ID required for concurrent test")

        import concurrent.futures

        def make_request():
            return authenticated_api.get_device_status(self.device_id)

        # Make multiple concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request) for _ in range(3)]
            results = [future.result() for future in futures]

        # Verify all requests succeeded
        assert len(results) == 3
        for result in results:
            assert isinstance(result, dict)
            assert "description" in result

import logging

import requests


class EmfitAPI:
    def __init__(self, token=None):
        self.base_url = "https://qs-api.emfit.com/api/v1"
        if token:
            self.token = token
        self.logger = logging.getLogger(__name__)

    def login(self, username, password):
        """
        Authenticates the user with the Emfit API using a POST request.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict: A JSON response containing the authentication token.

        Raises:
            Exception: If the login request fails and does not return a status code of 200.
        """
        data = {"username": username, "password": password}
        url = self.base_url + "/login"
        self.logger.info(f"Attempting to login user: {username}")
        response = requests.post(url, data=data)
        if response.status_code != 200:
            self.logger.error(
                f"Login failed with status code {response.status_code} for user: {username}"
            )
            raise Exception(f"Login failed with status code {response.status_code}")
        json_response = response.json()
        self.token = json_response["token"]
        self.logger.info(f"User {username} logged in successfully.")
        return json_response

    def handle_request(self, url, method="get", **kwargs):
        """
        Sends a request to the specified URL with the necessary authorization headers.

        Args:
            url (str): The URL to which the request is sent.
            method (str): The HTTP method to use ('get', 'post', etc.).
            **kwargs: Arbitrary keyword arguments that are passed to the requests function.

        Returns:
            dict: A JSON response from the API.

        Raises:
            Exception: If the request does not return a status code of 200.
        """
        headers = {"Authorization": f"Bearer {self.token}"}
        self.logger.info(f"Sending {method.upper()} request to {url}")
        response = requests.request(method, url, headers=headers, **kwargs)
        if response.status_code != 200:
            self.logger.error(
                f"Request to {url} failed with status code {response.status_code}"
            )
            raise Exception(f"Request failed with status code {response.status_code}")
        try:
            json_response = response.json()
        except ValueError as e:
            self.logger.error(f"Failed to parse JSON response for {url}: {e}")
            raise
        self.logger.info(
            f"Request to {url} succeeded with status code {response.status_code}"
        )
        return json_response

    def get_user(self, **kwargs):
        """
        Retrieves the user information from the Emfit API.

        Args:
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the user information.
        """
        url = self.base_url + "/user/get"
        self.logger.info(f"Retrieving user information from {url}")
        response = self.handle_request(url, **kwargs)
        self.logger.debug("User information retrieved successfully.")
        return response

    def get_device_status(self, device_id, **kwargs):
        """
        Retrieves the status of a specific device from the Emfit API.

        Args:
            device_id (str): The unique identifier of the device.
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the device status information.
        """
        url = self.base_url + f"/device/status/{device_id}"
        self.logger.info(
            f"Retrieving device status for device ID: {device_id} from {url}"
        )
        response = self.handle_request(url, **kwargs)
        self.logger.debug(
            f"Device status for device ID: {device_id} retrieved successfully."
        )
        return response

    def get_device_info(self, device_id, **kwargs):
        """
        Retrieves the information of a specific device from the Emfit API.

        Args:
            device_id (str): The unique identifier of the device.
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the device information.
        """
        url = self.base_url + f"/device/{device_id}"
        self.logger.info(
            f"Retrieving device information for device ID: {device_id} from {url}"
        )
        response = self.handle_request(url, **kwargs)
        self.logger.debug(
            f"Device information for device ID: {device_id} retrieved successfully."
        )
        return response

    def get_latest_presence(self, device_id, **kwargs):
        """
        Retrieves the latest presence information for a specific device from the Emfit API.

        Args:
            device_id (str): The unique identifier of the device.
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the latest presence information.
        """
        url = self.base_url + f"/presence/{device_id}/latest"
        self.logger.info(
            f"Retrieving latest presence information for device ID: {device_id} from {url}"
        )
        response = self.handle_request(url, **kwargs)
        self.logger.debug(
            f"Latest presence information for device ID: {device_id} retrieved successfully."
        )
        return response

    def get_presence(self, device_id, presence_id, **kwargs):
        """
        Retrieves the presence information for a specific device and presence ID from the Emfit API.

        Args:
            device_id (str): The unique identifier of the device.
            presence_id (str): The unique identifier of the presence event.
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the presence information.
        """
        url = self.base_url + f"/presence/{device_id}/{presence_id}"
        self.logger.info(
            f"Retrieving presence information for device ID: {device_id} and presence ID: {presence_id} from {url}"
        )
        response = self.handle_request(url, **kwargs)
        self.logger.debug(
            f"Presence information for device ID: {device_id} and presence ID: {presence_id} retrieved successfully."
        )
        return response

    def get_trends(self, device_id, start_date, end_date, **kwargs):
        """
        Retrieves the trends data for a specific device within the given date range from the Emfit API.

        Args:
            device_id (str): The unique identifier of the device.
            start_date (str): The start date of the period for which trends data is requested.
            end_date (str): The end date of the period for which trends data is requested.
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the trends data.
        """
        url = self.base_url + f"/trends/{device_id}/{start_date}/{end_date}"
        self.logger.info(
            f"Retrieving trends data for device ID: {device_id} from {start_date} to {end_date} from {url}"
        )
        response = self.handle_request(url, **kwargs)
        self.logger.debug(
            f"Trends data for device ID: {device_id} from {start_date} to {end_date} retrieved successfully."
        )
        return response

    def get_timeline(self, device_id, start_date, end_date, **kwargs):
        """
        Retrieves the timeline data for a specific device within the given date range from the Emfit API.

        Args:
            device_id (str): The unique identifier of the device.
            start_date (str): The start date of the period for which timeline data is requested.
            end_date (str): The end date of the period for which timeline data is requested.
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the timeline data.
        """
        url = self.base_url + f"/timeline/{device_id}/{start_date}/{end_date}"
        self.logger.info(
            f"Retrieving timeline data for device ID: {device_id} from {start_date} to {end_date} from {url}"
        )
        response = self.handle_request(url, **kwargs)
        self.logger.debug(
            f"Timeline data for device ID: {device_id} from {start_date} to {end_date} retrieved successfully."
        )
        return response

    def get_notification_settings(self, device_id, **kwargs):
        """
        Retrieves the notification settings for a specific device from the Emfit API.

        Args:
            device_id (str): The unique identifier of the device.
            **kwargs: Arbitrary keyword arguments that are passed to the handle_request() method.

        Returns:
            dict: A JSON response containing the notification settings.
        """
        url = self.base_url + f"/device/notification-settings/{device_id}"
        self.logger.info(
            f"Retrieving notification settings for device ID: {device_id} from {url}"
        )
        response = self.handle_request(url, **kwargs)
        self.logger.debug(
            f"Notification settings for device ID: {device_id} retrieved successfully."
        )
        return response

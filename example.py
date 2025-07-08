import logging
import os

from dotenv import load_dotenv

from emfit.api import EmfitAPI

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to execute the Emfit API interactions.
    It performs the following actions:
    - Retrieves environment variables for authentication and device identification.
    - Logs into the Emfit API and fetches user and device information.
    - Logs the latest sleep duration data for a specified device.
    - Fetches and logs detailed sleep data for the latest recorded period.
    """
    # Get environment variables
    username = os.getenv("EMFIT_USERNAME")
    password = os.getenv("EMFIT_PASSWORD")
    token = os.getenv("EMFIT_TOKEN")
    device_id = os.getenv("EMFIT_DEVICE_ID")

    # Create an API instance
    api = EmfitAPI(token)

    # Login and fetch data
    login_response = api.login(username, password)
    logger.debug(f"Login Response: {login_response}")

    user_info = api.get_user()
    logger.info(f"User Information: {user_info['user']['email']}")

    device_info = api.get_device_info(device_id)
    logger.info(f"Device Name: {device_info['device_name']}")

    device_status = api.get_device_status(device_id)
    logger.info(f"Device Status: {device_status['description']}")

    device_latest_presence = api.get_latest_presence(device_id)
    sleep_hours = device_latest_presence["sleep_duration"] / 3600
    logger.info(f"Device Latest Sleep Duration: {sleep_hours} hours")

    period_id = device_latest_presence["navigation_data"][-1]["id"]
    logger.debug(f"Period ID: {period_id}")

    sleep_data = api.get_presence(device_id, period_id)
    sleep_data_hours = sleep_data["sleep_duration"] / 3600
    logger.info(
        f"Sleep Data for {sleep_data['from_utc']} to {sleep_data['to_utc']} UTC: {sleep_data_hours} hours"
    )


if __name__ == "__main__":
    main()

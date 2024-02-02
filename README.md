# EmfitAPI Python Wrapper

## Overview

EmfitAPI is a Python wrapper for the Emfit QS API. It provides methods to authenticate, fetch user and device data, and retrieve various metrics such as presence, trends, and timeline data from Emfit devices.

## Installation

To use the EmfitAPI wrapper, you need Python installed on your system. Clone the repository and install the required packages:

```
git clone https://github.com/harperreed/emfitapi-python.git
cd emfitapi-python
pip install -r requirements.txt
```

## Usage

### Initializing the API

To start using the EmfitAPI, you need to instantiate the class:

```python
from emfit.api import EmfitAPI

api = EmfitAPI(token="your_token_here")
```

If you don't have a token, you can obtain one by logging in:

```python
api = EmfitAPI()
response = api.login("your_username", "your_password")
```

### Making Requests

After authentication, you can use various methods to interact with the API:

- `get_user()`: Fetches user information.
- `get_device_status(device_id)`: Retrieves the status of a specific device.
- `get_device_info(device_id)`: Fetches information of a specific device.
- `get_latest_presence(device_id)`: Gets the latest presence information for a device.
- `get_presence(device_id, presence_id)`: Retrieves presence information for a specific device and presence ID.
- `get_trends(device_id, start_date, end_date)`: Fetches trend data for a device within a specified date range.
- `get_timeline(device_id, start_date, end_date)`: Retrieves timeline data for a device within a specified date range.
- `get_notification_settings(device_id)`: Gets the notification settings for a specific device.

### Example

```python
# Retrieve and print user information
user_info = api.get_user()
print(user_info)

# Fetch and print device status
device_status = api.get_device_status("device_id_here")
print(device_status)
```

## Logging

EmfitAPI uses Python's logging module to log information, warnings, and errors. Configure the logging level as needed.

## Exception Handling

The wrapper raises exceptions when API requests fail. Ensure to handle these exceptions in your application.

# EmfitAPI Python Wrapper

[![CI](https://github.com/harperreed/emfitapi-python/workflows/CI/badge.svg)](https://github.com/harperreed/emfitapi-python/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/harperreed/emfitapi-python/branch/main/graph/badge.svg)](https://codecov.io/gh/harperreed/emfitapi-python)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

EmfitAPI is a Python wrapper for the Emfit QS API. It provides methods to authenticate, fetch user and device data, and retrieve various metrics such as presence, trends, and timeline data from Emfit devices.

## Installation

You can install the EmfitAPI wrapper using pip:

```bash
pip install git+https://github.com/harperreed/emfitapi-python.git
```

Or, if you've downloaded the source:

```bash
git clone https://github.com/harperreed/emfitapi-python.git
cd emfitapi-python
pip install .
```

### Development Installation

For development, we recommend using [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/harperreed/emfitapi-python.git
cd emfitapi-python
uv sync --all-extras
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

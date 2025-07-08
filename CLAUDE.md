# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python wrapper for the Emfit QS API that provides access to sleep tracking data from Emfit devices. The library handles authentication, device management, and data retrieval from the Emfit cloud service.

## Architecture

The project follows a simple, single-class architecture:

- `emfit/api.py`: Main `EmfitAPI` class that handles all API interactions
- `emfit/__init__.py`: Package initialization (currently empty)
- `example.py`: Demonstrates typical usage patterns with environment variables

### Core Components

**EmfitAPI Class** (`emfit/api.py`):
- Handles authentication via username/password login or direct token
- Implements a centralized `handle_request()` method for all API calls
- Provides methods for each API endpoint (user, device, presence, trends, timeline)
- Uses Python's `requests` library for HTTP communication
- Implements comprehensive logging for debugging and monitoring

**Key Methods**:
- `login(username, password)`: Authenticate and obtain bearer token
- `handle_request(url, method, **kwargs)`: Central request handler with auth headers
- `get_user()`: Retrieve user information and devices
- `get_device_status(device_id)`: Get current device status
- `get_latest_presence(device_id)`: Get most recent sleep data
- `get_presence(device_id, presence_id)`: Get specific sleep period data
- `get_trends()` and `get_timeline()`: Get historical data over date ranges

## Development Commands

### Environment Setup
```bash
# Install dependencies
uv sync

# Run example script
uv run example.py
```

### Testing
There are currently no tests in this project. Any test implementation should cover:
- Authentication flows (login, token handling)
- API request/response handling
- Error handling for failed requests
- Data parsing and validation

### Package Management
This project uses `uv` for dependency management. Dependencies are defined in `pyproject.toml`:
- `requests`: HTTP client library
- `python-dotenv`: Environment variable management

## Environment Variables

The example script expects these environment variables:
- `EMFIT_USERNAME`: User's Emfit account username
- `EMFIT_PASSWORD`: User's Emfit account password
- `EMFIT_TOKEN`: Direct API token (alternative to username/password)
- `EMFIT_DEVICE_ID`: Device ID for data retrieval

## API Integration

The Emfit QS API base URL is: `https://qs-api.emfit.com/api/v1`

**Authentication**: Bearer token required for all requests except login
**Data Format**: All responses are JSON
**Error Handling**: Non-200 status codes raise exceptions with descriptive messages

Key data structures include sleep metrics (duration, efficiency, score), sleep stages (awake, deep, light, REM), and physiological metrics (heart rate, respiratory rate, activity).

## Code Patterns

- All API methods follow the same pattern: construct URL, call `handle_request()`, return JSON response
- Comprehensive logging at INFO level for operations, DEBUG for detailed responses
- Exception handling with descriptive error messages
- Method signatures use `**kwargs` to allow flexible request parameters
- Token management is handled automatically after login

## File Structure
```
emfit/
├── __init__.py          # Package initialization
└── api.py              # Main EmfitAPI class
example.py              # Usage example with environment variables
API.md                  # Detailed API documentation
```

This is a straightforward wrapper library focused on providing clean, Pythonic access to the Emfit QS API with proper error handling and logging.

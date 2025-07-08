# Emfit QS API Documentation

## Base URL

```
https://qs-api.emfit.com/api/v1
```

## Authentication

### Login

Authenticate with the API to receive a bearer token.

**Endpoint:** `/login`
**Method:** POST
**Request Body:**

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "remember_token": "$2y$10$9IE/.MmEscA41UQ2...",
    "user": {
        "id": 5065,
        "username": "0011A7",
        "email": "user@example.com",
        "locale": "en_US",
        "timezone_id": 382,
        "gmt_offset": -21600,
        "devices": "4613,4470",
        "timezone_name": "America/Chicago",
        "subscription": true,
        "verified_email": true,
        "agreement": true,
        "consent": false
    }
}
```

All subsequent requests must include the bearer token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## User Endpoints

### Get User Information

Retrieve information about the authenticated user.

**Endpoint:** `/user/get`
**Method:** GET
**Response:**

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 5065,
        "username": "0011A7",
        "email": "user@example.com",
        "locale": "en_US",
        "timezone_id": 382,
        "gmt_offset": -21600,
        "devices": "4613,4470",
        "timezone_name": "America/Chicago",
        "subscription": true,
        "verified_email": true
    },
    "notification_settings": {
        "4470": {
            "device_id": "4470",
            "sms_alert": false,
            "email_alert": false,
            "alarm_profile": "off",
            "morning_alarm": false,
            "morning_alarm_time": "07:00"
            // ... additional settings
        }
    },
    "device_settings": [
        {
            "device_id": "4470",
            "serial_number": "001122",
            "device_name": "Device Name",
            "firmware": "120.2.2.1",
            "enabled_hrv": true
            // ... additional settings
        }
    ]
}
```

## Device Endpoints

### Get Device Information

Retrieve information about a specific device.

**Endpoint:** `/device/{device_id}`
**Method:** GET
**Response:**

```json
{
    "field1": "left side",
    "field2": null,
    "device_name": "Device Name",
    "firmware": "120.2.2.1"
}
```

### Get Device Status

Get the current status of a specific device.

**Endpoint:** `/device/status/{device_id}`
**Method:** GET
**Response:**

```json
{
    "device_index": "4613",
    "description": "absent",
    "from": 1730813827000
}
```

### Get Device Notification Settings

Retrieve notification settings for a specific device.

**Endpoint:** `/device/notification-settings/{device_id}`
**Method:** GET
**Response:**

```json
{
    "device_id": "4470",
    "sms_alert": false,
    "email_alert": false,
    "alarm_profile": "off",
    "morning_alarm": false,
    "morning_alarm_time": "07:00"
    // ... additional settings
}
```

## Presence Data Endpoints

### Get Latest Presence

Retrieve the most recent presence data for a device.

**Endpoint:** `/presence/{device_id}/latest`
**Method:** GET
**Response:**

```json
{
    "id": "672a1f93d41d8c004324905d",
    "device_id": "4613",
    "time_start": 1730780520,
    "time_end": 1730813820,
    "sleep_duration": 27240,
    "sleep_efficiency": 83,
    "sleep_score": 84,
    "sleep_score_2": 100,
    "sleep_class_awake_duration": 6030,
    "sleep_class_deep_duration": 5400,
    "sleep_class_light_duration": 13410,
    "sleep_class_rem_duration": 8430,
    "measured_hr_avg": 54,
    "measured_rr_avg": 17,
    "measured_activity_avg": 160,
    "bed_exit_count": 3,
    "tossnturn_count": 127,
    "from_utc": "2024-11-05 04:22:00",
    "to_utc": "2024-11-05 13:37:00",
    "minitrend_datestamps": [],
    "minitrend_sleep_score": [],
    "minitrend_sleep_efficiency": []
    // ... additional trend data
}
```

### Get Specific Presence Data

Retrieve presence data for a specific period.

**Endpoint:** `/presence/{device_id}/{presence_id}`
**Method:** GET
**Response:** Similar to Latest Presence response

## Trends and Timeline Endpoints

### Get Trends

Retrieve trend data for a specific date range.

**Endpoint:** `/trends/{device_id}/{start_date}/{end_date}`
**Method:** GET

### Get Timeline

Retrieve timeline data for a specific date range.

**Endpoint:** `/timeline/{device_id}/{start_date}/{end_date}`
**Method:** GET

## Data Structures

### Sleep Metrics

-   `sleep_duration`: Total sleep duration in seconds
-   `sleep_efficiency`: Sleep efficiency percentage
-   `sleep_score`: Overall sleep score (0-100)
-   `sleep_score_2`: Alternative sleep score calculation (0-100)
-   `sleep_onset_duration`: Time taken to fall asleep in seconds

### Sleep Stages

-   `sleep_class_awake_duration`: Time spent awake in seconds
-   `sleep_class_deep_duration`: Time in deep sleep in seconds
-   `sleep_class_light_duration`: Time in light sleep in seconds
-   `sleep_class_rem_duration`: Time in REM sleep in seconds
-   `sleep_class_awake_percent`: Percentage of time spent awake
-   `sleep_class_deep_percent`: Percentage in deep sleep
-   `sleep_class_light_percent`: Percentage in light sleep
-   `sleep_class_rem_percent`: Percentage in REM sleep

### Physiological Metrics

-   `measured_hr_avg`: Average heart rate
-   `measured_hr_min`: Minimum heart rate
-   `measured_hr_max`: Maximum heart rate
-   `measured_rr_avg`: Average respiratory rate
-   `measured_rr_min`: Minimum respiratory rate
-   `measured_rr_max`: Maximum respiratory rate
-   `measured_activity_avg`: Average activity level

### Sleep Quality Indicators

-   `bed_exit_count`: Number of times user left bed
-   `bed_exit_periods`: Array of [start, end] timestamps for bed exits
-   `tossnturn_count`: Number of restless movements
-   `tossnturn_datapoints`: Array of timestamps for movements

## Error Handling

The API returns standard HTTP status codes:

-   200: Success
-   400: Bad Request
-   401: Unauthorized
-   403: Forbidden
-   404: Not Found
-   500: Internal Server Error

All errors will include a descriptive message in the response body.

## Rate Limiting

Information about rate limiting is not provided in the API logs. Contact Emfit support for details about rate limiting policies.

## Timezone Handling

-   All timestamps in responses are Unix timestamps (seconds since epoch)
-   The API provides both UTC timestamps (`from_utc`, `to_utc`) and local time strings (`time_start_string`, `time_end_string`)
-   User timezone information is included in user data (`gmt_offset`, `timezone_name`)

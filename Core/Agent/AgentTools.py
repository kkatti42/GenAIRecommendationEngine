import requests
from langchain.tools import tool
from typing import Union, Dict, Any

# Helper class to fetch weather data and itemization data via API
# These are tools only used when running the application using AGENT

@tool
def get_weather_data_tool(zip_code: str) -> Union[Dict[str, Any], str]:
    """
    Fetches current weather data for a given US ZIP code from API.

    Args:
        zip_code (str): The 5-digit US ZIP code.

    Returns:
        dict: The filtered JSON response if the call succeeds.
        str: An error message if something goes wrong.
    """

    print("Fetching Weather Data..")

    url = f"{url}/weather/US/{zip_code}"
    headers = {
        "Authorization": "Bearer {token}"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()

        data = resp.json()
        cutoff_timestamp = 1745988894

        # Filter response by timestamp
        filtered_data = {
            k: v for k, v in data.items()
            if int(k) > cutoff_timestamp
        }

        return filtered_data

    except requests.HTTPError as http_err:
        print(f"HTTP error fetching weather for {zip_code}: {http_err}")
    except Exception as e:
        print(f"Error fetching weather for {zip_code}: {e}")
    return

@tool
def get_itemization_data_tool(input: str) -> Union[Dict[str, Any], str]:
    """
    Fetches itemization data from API.

    Args:
        start (str): Start date in YYYY-MM-DD format.
        end (str): End date in YYYY-MM-DD format.

    Returns:
        dict: The parsed JSON response if the call succeeds.
        str: An error message if something goes wrong.
    """

    params = json.loads(input)
    start = params["start"]
    end = params["end"]

    url = (
        "{url}/v2.0/users/{userid}/endpoints/"
        "{id}/itemizationDetails?"
        f"fromDate={start}&toDate={end}&extended=true&hybrid=true&mode=month&"
        "round=true"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()

    except requests.HTTPError as http_err:
        return f"HTTP error fetching data: {http_err}"
    except Exception as e:
        return f"Error fetching data: {e}"
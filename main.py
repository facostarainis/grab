import requests
import json
from datetime import datetime, timezone
import os

def fetch_data(payload):
    url = "https://www.grab.com/wp-json/api/farefeed/v1/estimate"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.grab.com",
        "Referer": "https://www.grab.com/ph/fare-check/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to fetch data. Status code: {response.status_code}"

def save_data(data_batch):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, "data_log.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append({"timestamp": datetime.now(timezone.utc).isoformat(), "data": data_batch})

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)

def main():
    payloads = [

        {"pickUp": {"latitude": 14.449087314184396,"longitude": 120.98081355043848,"address": "Alabang-Zapote Road, Pamplona Dos, Las Pinas City, Metro Manila, 1740, National Capital Region (Ncr), Philippines"},
        "dropOff": {"latitude": 14.5494146936948,"longitude": 121.0287934877,"address": "Edsa, Dasmarinas, Makati City, Metro Manila, 1224, National Capital Region (Ncr), Philippines"}},
        
        {"pickUp": {"latitude": 14.515634806818525,"longitude": 120.98135176074652,"address": "Seaside Dr cor J. W. Diokno Blvd, Tambo, Paranaque City cor J. W. Diokno Blvd, Tambo, Paranaque City, Metro Manila, 1701, National Capital Region (Ncr), Philippines"},
        "dropOff": {"latitude": 14.5494146936948,"longitude": 121.0287934877,"address": "Edsa, Dasmarinas, Makati City, Metro Manila, 1224, National Capital Region (Ncr), Philippines"}},
        
        # Your 10 different payloads here
        # Example: {"pickUp": {...}, "dropOff": {...}}, ...
    ]

    data_batch = []
    for payload in payloads:
        data = fetch_data(payload)
        data_batch.append(data)

    save_data(data_batch)

if __name__ == "__main__":
    main()

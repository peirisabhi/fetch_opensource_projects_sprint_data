import requests
import pandas as pd
import time
import json

from requests.auth import HTTPBasicAuth


USERNAME = "feenionloyed"
PASSWORD = "2001adp@549"

# Store all data
all_boards = []
all_sprints = []
all_issues = []
all_backlog_issues = []

# Get all boards
def fetch_all_boards():
    boards = []
    start_at = 0
    max_results = 50
    is_last = False

    while not is_last:
        url = f"https://issues.apache.org/jira/rest/agile/1.0/board?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.status_code != 200:
            print(f"Error fetching boards: {response.status_code}")
            break

        data = response.json()
        boards.extend(data['values'])
        is_last = data['isLast']
        start_at += max_results
        time.sleep(1)  # Respect rate limits

    return boards



if __name__ == '__main__':
    print("Fetching all boards...")
    boards = fetch_all_boards();
    print(f"Found {len(boards)} boards")
    print(boards)
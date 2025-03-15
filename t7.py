import requests
import pandas as pd
import time
import json

from requests.auth import HTTPBasicAuth

# You might need authentication
headers = {
    'Accept': 'application/json'
    # Add any required authentication headers
}

USERNAME = "feenionloyed"
PASSWORD = "2001adp@549"

# response = requests.get(JIRA_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))

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
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.status_code != 200:
            print(f"Error fetching boards: {response.status_code}")
            break

        data = response.json()
        boards.extend(data['values'])
        is_last = data['isLast']
        start_at += max_results
        time.sleep(1)  # Respect rate limits

    return boards


# Get sprints for a board
def fetch_sprints(board_id):
    sprints = []
    start_at = 0
    max_results = 50
    is_last = False

    while not is_last:
        url = f"https://issues.apache.org/jira/rest/agile/1.0/board/{board_id}/sprint?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.status_code != 200:
            # Some boards may not have sprints or might be inaccessible
            print(f"Error fetching sprints for board {board_id}: {response.status_code}")
            break

        try:
            data = response.json()
            sprints.extend(data['values'])
            is_last = data.get('isLast', True)
            start_at += max_results
        except:
            break

        time.sleep(1)  # Respect rate limits

    return sprints


# Get issues for a sprint
def fetch_sprint_issues(board_id, sprint_id):
    issues = []
    start_at = 0
    max_results = 50
    is_last = False

    while not is_last:
        url = f"https://issues.apache.org/jira/rest/agile/1.0/board/{board_id}/sprint/{sprint_id}/issue?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.status_code != 200:
            print(f"Error fetching issues for board {board_id}, sprint {sprint_id}: {response.status_code}")
            break

        try:
            data = response.json()
            issues.extend(data['issues'])
            is_last = data.get('isLast', True)
            start_at += max_results
        except:
            break

        time.sleep(1)  # Respect rate limits

    return issues


# Get backlog issues
def fetch_backlog_issues(board_id):
    issues = []
    start_at = 0
    max_results = 50
    is_last = False

    while not is_last:
        url = f"https://issues.apache.org/jira/rest/agile/1.0/board/{board_id}/backlog?startAt={start_at}&maxResults={max_results}"
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        if response.status_code != 200:
            print(f"Error fetching backlog for board {board_id}: {response.status_code}")
            break

        try:
            data = response.json()
            issues.extend(data['issues'])
            is_last = data.get('isLast', True)
            start_at += max_results
        except:
            break

        time.sleep(1)  # Respect rate limits

    return issues


# Main execution
print("Fetching all boards...")
all_boards = fetch_all_boards()
print(f"Found {len(all_boards)} boards")

# Optional: Limit the number of boards to process if you only need a sample
boards_to_process = all_boards[:20]  # Process first 20 boards

for board in boards_to_process:
    board_id = board['id']
    print(f"Processing board: {board['name']} (ID: {board_id})")

    # Get sprints
    sprints = fetch_sprints(board_id)
    for sprint in sprints:
        sprint['boardId'] = board_id
        all_sprints.append(sprint)

        # Get issues for this sprint
        sprint_id = sprint['id']
        issues = fetch_sprint_issues(board_id, sprint_id)
        for issue in issues:
            issue['boardId'] = board_id
            issue['sprintId'] = sprint_id
            all_issues.append(issue)

    # Get backlog issues
    backlog = fetch_backlog_issues(board_id)
    for issue in backlog:
        issue['boardId'] = board_id
        issue['isBacklog'] = True
        all_backlog_issues.append(issue)

# Save to files
with open('apache_boards.json', 'w') as f:
    json.dump(all_boards, f)

with open('apache_sprints.json', 'w') as f:
    json.dump(all_sprints, f)

with open('apache_sprint_issues.json', 'w') as f:
    json.dump(all_issues, f)

with open('apache_backlog_issues.json', 'w') as f:
    json.dump(all_backlog_issues, f)

# Create DataFrames for analysis
boards_df = pd.json_normalize(all_boards)
sprints_df = pd.json_normalize(all_sprints)
issues_df = pd.json_normalize(all_issues)
backlog_df = pd.json_normalize(all_backlog_issues)

# Save as CSV
boards_df.to_csv('apache_boards.csv', index=False)
sprints_df.to_csv('apache_sprints.csv', index=False)
issues_df.to_csv('apache_sprint_issues.csv', index=False)
backlog_df.to_csv('apache_backlog_issues.csv', index=False)

print(
    f"Collected {len(all_boards)} boards, {len(all_sprints)} sprints, {len(all_issues)} sprint issues, {len(all_backlog_issues)} backlog issues")
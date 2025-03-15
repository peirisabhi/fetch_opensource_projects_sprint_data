import requests

PROJECT_KEY = "SPARK"  # Change this to your project's key
JIRA_BOARDS_URL = f"https://issues.apache.org/jira/rest/agile/1.0/board?projectKeyOrId={PROJECT_KEY}"

response = requests.get(JIRA_BOARDS_URL)

if response.status_code == 200:
    boards = response.json()["values"]
    for board in boards:
        print(f"Board ID: {board['id']}, Name: {board['name']}, Type: {board['type']}")
else:
    print(f"Error: {response.status_code}, {response.text}")

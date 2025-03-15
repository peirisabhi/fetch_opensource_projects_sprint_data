import requests
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://issues.apache.org/jira/rest/agile/1.0/board"

USERNAME = "feenionloyed@gmail.com"
PASSWORD = "2001adp@54"

response = requests.get(JIRA_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))


# response = requests.get(JIRA_URL)

if response.status_code == 200:
    boards = response.json()["values"]
    for board in boards:
        print(f"Board ID: {board['id']} - Name: {board['name']} - Type: {board['type']}")
else:
    print(f"Error: {response.status_code}, {response.text}")

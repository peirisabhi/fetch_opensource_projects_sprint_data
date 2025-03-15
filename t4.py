import requests

PROJECT_KEY = "SPARK"
JIRA_SPRINTS_URL = "https://issues.apache.org/jira/rest/agile/1.0/board/1/sprint/search?jql=project={PROJECT_KEY}"

response = requests.get(JIRA_SPRINTS_URL)

if response.status_code == 200:
    sprints = response.json().get("values", [])
    for sprint in sprints:
        print(f"Sprint ID: {sprint['id']}, Name: {sprint['name']}, State: {sprint['state']}")
else:
    print(f"Error: {response.status_code}, {response.text}")

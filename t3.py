import requests

# Replace with the project key (e.g., "MESOS", "HADOOP", "SPARK")
PROJECT_KEY = "MESOS"
# JIRA_ISSUES_URL = f"https://issues.apache.org/jira/rest/api/2/search?jql=project={PROJECT_KEY} AND sprint IS NOT EMPTY"
JIRA_ISSUES_URL = f"https://issues.apache.org/jira/rest/api/2/search?jql=project={PROJECT_KEY} AND sprint=2"

response = requests.get(JIRA_ISSUES_URL)

if response.status_code == 200:
    issues = response.json()["issues"]
    print(len(issues))
    for issue in issues[:10]:  # Fetch first 10 issues
        # print(f"Issue: {issue['key']} - {issue['fields']['summary']}")
        print(issue)
else:
    print(f"Error: {response.status_code}, {response.text}")

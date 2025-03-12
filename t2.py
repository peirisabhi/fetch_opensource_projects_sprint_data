import requests

# Jira API URL (Replace with actual Jira instance URL)
JIRA_URL = "https://jira.spring.io/rest/api/2/search"

# JQL query to fetch Spring XD issues (Modify if needed)
query = {
    "jql": 'project = "XD" ORDER BY created DESC',
    "maxResults": 10,  # Limit results
    "fields": ["key", "summary", "status", "created"]
}

# Make GET request
response = requests.get(JIRA_URL, params=query)

if response.status_code == 200:
    data = response.json()
    for issue in data.get("issues", []):
        print(f"Issue: {issue['key']} - {issue['fields']['summary']} (Status: {issue['fields']['status']['name']})")
else:
    print(f"Error: Unable to fetch issues (Status Code: {response.status_code})")

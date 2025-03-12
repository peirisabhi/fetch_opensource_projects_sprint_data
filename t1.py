from jira import JIRA

# Connect to Jira (replace with actual Jira instance)
JIRA_SERVER = "https://jira.spring.io"  # Check if this is still active
jira = JIRA(server=JIRA_SERVER)

# Fetch issues related to Spring-XD (modify the query if needed)
jql_query = 'project = "XD" ORDER BY created DESC'
issues = jira.search_issues(jql_query, maxResults=10)  # Adjust maxResults

# Print issue details
for issue in issues:
    print(f"Issue: {issue.key} - {issue.fields.summary}")

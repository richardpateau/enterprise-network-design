import os
import requests
from requests.auth import HTTPBasicAuth
import json
JIRA_URL = "https://richardpateau74.atlassian.net"
JIRA_EMAIL = "richardpateau74@gmail.com"
JIRA_API_TOKEN = "ATATT3xFfGF0pmfyQrjOYssYZkuPCgj2cYHX4zv-ZBTf_ELbM_-c70ChfwKzghYPpzpwGwQm9e5F1A1zyEBRFx18HhR6RapRTsm7MkwwDj8cCDMrUxk5SBYcAkOnVpNjLxvqhkv0T55v1YjZ9pz4gFT_lGvpzWLpGbo-ZtRyqQKSxv3YOIDgbbw=8CBB0238"


session = requests.Session()
session.auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
			"Accept": "application/json",
			"Content-Type": "application/json"
		}

#jira_query = f"project = SUP AND status = 'To do' AND summary ~ 'Port Provisioning' ORDER BY created ASC"
jira_query = f"project = SUP AND status = 'Open' AND summary ~ 'Port Provisioning' ORDER BY created ASC"
endpoint_url = f"https://richardpateau74.atlassian.net/rest/api/3/search/jql"
parameters = {
    "jql": jira_query,
    "maxResults": 10,
    "fields": "summary,description,status"
}

response = requests.get(endpoint_url, auth=session.auth, headers=headers, params=parameters)

data = response.json()
print(json.dumps(data, indent=4))

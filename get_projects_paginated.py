#! /usr/bin/env python
"""GET - Get projects paginated.

Returns a paginated list of projects visible to the user.
This operation can be accessed anonymously.
Permissions required: Projects are returned only where the user has one of:

- Browse Projects project permission for the project.
- Administer Projects project permission for the project.
- Administer Jira global permission.

Data Security Policy: Not exempt from app access rules

## Scopes

Connect app scope required: READ
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:issue-type:jira, read:project:jira, read:project.property:jira,
    read:user:jira, read:application-role:jira, read:avatar:jira,
    read:group:jira, read:issue-type-hierarchy:jira, read:project-category:jira,
    read:project-version:jira, read:project.component:jira(Show less)
"""
import json
import os

import requests
from requests.auth import HTTPBasicAuth

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/project/search'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))

#! /usr/bin/env python
"""GET - Get workflows paginated.

Returns a paginated list of published classic workflows. When workflow names are specified, details of those workflows are returned. Otherwise, all published classic workflows are returned.

This operation does not return next-gen workflows.
Permissions required: Administer Jira global permission.
Data Security Policy: Exempt from app access rules

## Scopes

Connect app scope required: ADMIN
OAuth 2.0 scopes required:
Classic RECOMMENDED: manage:jira-project
Granular:
    read:group:jira, read:issue-security-level:jira, read:project-role:jira,
    read:screen:jira, read:status:jira, read:user:jira, read:workflow:jira,
    read:webhook:jira, read:avatar:jira, read:project-category:jira, read:project:jira

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

url = f'{API_BASE_URL}/rest/api/3/workflow/search'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))

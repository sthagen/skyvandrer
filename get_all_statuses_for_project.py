#! /usr/bin/env python
"""GET - Get all statuses for project.

Returns the valid statuses for a project. The statuses are grouped by issue type,
as each project has a set of valid issue types and each issue type has a set of valid statuses.

This operation can be accessed anonymously.

Permissions required: Browse Projects project permission for the project.
Data Security Policy: Exempt from app access rules

## Scopes

Connect app scope required: READ
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:issue-status:jira, read:issue-type:jira, read:status:jira

"""

import json
import os
import sys

import requests
from requests.auth import HTTPBasicAuth

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

try:
    project_id_or_key = sys.argv[1]
except IndexError as err:
    raise Exception('missing project id or key') from err

url = f'{API_BASE_URL}/rest/api/3/project/{project_id_or_key}/statuses'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))

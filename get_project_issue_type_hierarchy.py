#! /usr/bin/env python
"""Get project issue type hierarchy (of ticket management system).

Get the issue type hierarchy for a next-gen project.

The issue type hierarchy for a project consists of:

- Epic at level 1 (optional).
- One or more issue types at level 0 such as Story, Task, or Bug.
  Where the issue type Epic is defined, these issue types are used to break down the content of an epic.
- Subtask at level -1 (optional).
  This issue type enables level 0 issue types to be broken down into components.
  Issues based on a level -1 issue type must have a parent issue.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-projectid-hierarchy-get>

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
    project_id = sys.argv[1]
except IndexError as err:
    raise Exception('missing project id') from err

try:
    _ = int(project_id)
except ValueError as err:
    raise Exception('invalid project id type - integer required') from err

url = f'{API_BASE_URL}/rest/api/3/project/{project_id}/hierarchy'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))

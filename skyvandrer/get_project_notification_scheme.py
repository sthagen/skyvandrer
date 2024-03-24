#! /usr/bin/env python
"""Get project notification scheme (of ticket management system).

Gets a notification scheme associated with the project.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-projectkeyorid-notificationscheme-get>

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

url = f'{API_BASE_URL}/rest/api/3/project/{project_id_or_key}/notificationscheme'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))

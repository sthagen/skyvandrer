#! /usr/bin/env python
"""Get all permissions (of ticket management system).

Returns all permissions, including:

- global permissions.
- project permissions.
- global permissions added by plugins.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permissions/#api-rest-api-3-permissions-get>

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

url = f'{API_BASE_URL}/rest/api/3/permissions'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)
data = json.loads(response.text)

print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

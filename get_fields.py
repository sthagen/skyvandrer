#! /usr/bin/env python
"""GET - Get fields.

Returns system and custom issue fields according to the following rules:

- Fields that cannot be added to the issue navigator are always returned.
- Fields that cannot be placed on an issue screen are always returned.
- Fields that depend on global Jira settings are only returned if the setting is enabled.
  That is, timetracking fields, subtasks, votes, and watches.
- For all other fields, this operation only returns the fields that the user has permission to view
  (that is, the field is used in at least one project that the user has Browse Projects project permission for.)

This operation can be accessed anonymously.
Permissions required: None.
Data Security Policy: Exempt from app access rules

## Scopes

Connect app scope required: READ
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:field:jira, read:avatar:jira, read:project-category:jira, read:project:jira, read:field-configuration:jira

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

url = f'{API_BASE_URL}/rest/api/3/field'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)
data = json.loads(response.text)

print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

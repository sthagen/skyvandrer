#! /usr/bin/env python
"""GET - Get fields paginated.

Returns a paginated list of fields for Classic Jira projects. The list can include:

- all fields
- specific fields, by defining id
- fields that contain a string in the field name or description, by defining query
- specific fields that contain a string in the field name or description, by defining id and query

Only custom fields can be queried, type must be set to custom.
Permissions required: Administer Jira global permission.
Data Security Policy: Exempt from app access rules

## Scopes

Connect app scope required: NONE
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:field:jira, read:field-configuration:jira
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

url = f'{API_BASE_URL}/rest/api/3/field/search'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))

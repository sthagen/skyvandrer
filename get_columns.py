#! /usr/bin/env python
"""GET - Get columns.

Returns the columns configured for a filter.
The column configuration is used when the filter's results are viewed in List View with the Columns set to Filter.
This operation can be accessed anonymously.
Permissions required: None, however, column details are only returned for:

- filters owned by the user.
- filters shared with a group that the user is a member of.
- filters shared with a private project that the user has Browse projects project permission for.
- filters shared with a public project.
- filters shared with the public.

Data Security Policy: Not exempt from app access rules

## Scopes

Connect app scope required: READ
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:filter.column:jira
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
    filter_id = sys.argv[1]
except IndexError as err:
    raise Exception('missing filter id') from err

try:
    _ = int(filter_id)
except ValueError as err:
    raise Exception('invalid filter id type - integer required') from err

url = f'{API_BASE_URL}/rest/api/3/filter/{filter_id}/columns'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

response = requests.request('GET', url, headers=headers, auth=auth)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(',', ': ')))

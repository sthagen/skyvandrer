#! /usr/bin/env python
"""Get columns (of ticket management system).

Returns the columns configured for a filter.
The column configuration is used when the filter's results are viewed in List View with the Columns set to Filter.
This operation can be accessed anonymously.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-filters/#api-rest-api-3-filter-id-columns-get>

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

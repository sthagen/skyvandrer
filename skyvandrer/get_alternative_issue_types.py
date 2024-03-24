#! /usr/bin/env python
"""Get alternative issue types (of ticket management system).

Returns all issue types.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/#api-rest-api-3-issuetype-id-alternatives-get>

"""
import json
import os
import sys
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

CollectorType = dict[str, Union[bool, int, str, None, dict[str, str], list[object]]]
QueryType = dict[str, Union[bool, int, str, list[str]]]

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

try:
    issue_type_id = sys.argv[1]
except IndexError as err:
    raise Exception('missing issue type id') from err

try:
    _ = int(issue_type_id)
except ValueError as err:
    raise Exception('invalid issue type id type - integer required') from err

url = f'{API_BASE_URL}/rest/api/3/issuetype/{issue_type_id}/alternatives'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query: QueryType = {}

collector: CollectorType = {
    'endpoint': url,
    'is_complete': False,
    'page_capacity': None,
    'roundtrip_count': 1,
    'offset': 0,
    'total_count': 0,
    'errors': [],
    'error_messages': [],
    'items': [],
}
response = requests.request('GET', url, headers=headers, params=query, auth=auth)
data = json.loads(response.text)

error_messages = []
try:
    error_messages = data.get('errorMessages', [])
except AttributeError:
    pass

if error_messages:
    for entry in error_messages:
        collector['error_messages'].append(entry)  # type: ignore
    errors = data.get('errors', [])
    for entry in errors:
        collector['errors'].append(entry)  # type: ignore
else:
    for entry in data:
        collector['items'].append(entry)  # type: ignore

collector['total_count'] = len(collector['items'])  # type: ignore
collector['is_complete'] = True


print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

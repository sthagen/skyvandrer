#! /usr/bin/env python
"""Get current user (of ticket management system).

Returns details for the current user.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-myself/#api-rest-api-3-myself-get>

"""
import json
import os
import re
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

CollectorType = dict[str, Union[bool, int, str, None, dict[str, str], list[object]]]
QueryType = dict[str, Union[bool, int, str, list[str]]]

QUERY_SEP = '&'
UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$')

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/myself'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query: QueryType = {
    'expand': 'groups,applicationRoles',
}

collector: CollectorType = {
    'endpoint': url,
    'query': {k: v for k, v in query.items() if k != 'startAt'},  # type: ignore
    'page_capacity': 0,
    'roundtrip_count': 0,
    'start_index': 0,
    'total_count': 0,
    'errors': [],
    'error_messages': [],
    'record': {},
}
response = requests.request('GET', url, headers=headers, params=query, auth=auth)  # type: ignore
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
    for k, v in data.items():
        collector['record'][k] = v  # type: ignore

collector['total_count'] = len(collector['record'])  # type: ignore
collector['is_complete'] = True

print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

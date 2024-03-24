#! /usr/bin/env python
"""Get all issue types for user (of ticket management system).

Returns all issue types.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-types/#api-rest-api-3-issuetype-get>

"""
import json
import os
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

url = f'{API_BASE_URL}/rest/api/3/issuetype'

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

for entry in data:
    collector['items'].append(entry)  # type: ignore

collector['total_count'] = len(collector['items'])  # type: ignore
collector['is_complete'] = True


print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

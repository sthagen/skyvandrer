#! /usr/bin/env python
"""Get audit records (of ticket management system).

Returns a list of audit records. The list can be filtered to include items:
- where each item in filter has at least one match in any of these fields:
  - summary
  - category
  - eventSource
  - objectItem.name If the object is a user, account ID is available to filter.
  - objectItem.parentName
  - objectItem.typeName
  - changedValues.changedFrom
  - changedValues.changedTo
  - remoteAddress
  
  For example, if filter contains man ed, an audit record containing summary":
  "User added to group" and "category": "group management" is returned.
  created on or after a date and time.
  created or or before a date and time.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-audit-records/#api-rest-api-3-auditing-record-get>

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

url = f'{API_BASE_URL}/rest/api/3/auditing/record'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query: QueryType = {
    'offset': 0,
    'limit': 1000,
}

collector: CollectorType = {
    'endpoint': url,
    'is_complete': False,
    'page_capacity': query['limit'],  # type: ignore
    'roundtrip_count': 1,
    'offset': 0,
    'total_count': 0,
    'errors': [],
    'error_messages': [],
    'items': [],
}
response = requests.request('GET', url, headers=headers, params=query, auth=auth)
data = json.loads(response.text)

error_messages = data.get('errorMessages', [])
if error_messages:
    for entry in error_messages:
        collector['error_messages'].append(entry)  # type: ignore
    errors = data.get('errors', [])
    for entry in errors:
        collector['errors'].append(entry)  # type: ignore
else:
    collector['total_count'] = data.get('total', 0)
    for entry in data.get('records', []):
        collector['items'].append(entry)  # type: ignore

collector['is_complete'] = True


print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

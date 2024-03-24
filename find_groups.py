#! /usr/bin/env python
"""Find groups (of ticket management system).

Returns a list of groups whose names contain a query string.
A list of group names can be provided to exclude groups from the results.

The primary use case for this resource is to populate a group picker suggestions list.
To this end, the returned object includes the html field where the matched query term is
highlighted in the group name with the HTML strong tag.
Also, the groups list is wrapped in a response object that contains a header for use in the picker,
specifically Showing X of Y matching groups.

The list returns with the groups sorted. If no groups match the list criteria, an empty list is returned.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-groups-picker-get>

"""
import json
import os
import sys
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

CollectorType = dict[str, Union[bool, int, str, None, dict[str, str], list[object]]]

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/groups/picker'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

try:
    query_string = sys.argv[1]
except IndexError as err:
    raise Exception('missing query string') from err

query = {
    'query': query_string,
    'caseInsensitive': True,
}

collector: CollectorType = {
    'endpoint': url,
    'query': {k: v for k, v in query.items()},  # type: ignore
    'total_count': 0,
    'summary_display': None,
    'errors': [],
    'error_messages': [],
    'items': [],
}

response = requests.request('GET', url, headers=headers, params=query, auth=auth)  # type: ignore
data = json.loads(response.text)

error_messages = data.get('errorMessages', [])
if error_messages:
    for entry in error_messages:
        collector['error_messages'].append(entry)  # type: ignore
    errors = data.get('errors', [])
    for entry in errors:
        collector['errors'].append(entry)  # type: ignore
else:
    collector['summary_display'] = data.get('header')
    for entry in data.get('groups'):
        collector['items'].append(entry)  # type: ignore

collector['total_count'] = len(collector['items'])  # type: ignore

print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

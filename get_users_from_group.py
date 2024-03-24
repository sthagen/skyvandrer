#! /usr/bin/env python
"""Get users from group (of ticket management system).

Returns a paginated list of all users in a group.
Note that users are ordered by username, however the username is not returned in the results due to privacy reasons.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-member-get>

"""
import json
import os
import re
import sys
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

CollectorType = dict[str, Union[bool, int, str, None, dict[str, str], list[object]]]
QueryType = dict[str, Union[int, str]]

UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$')

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/group/member'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

try:
    group_id_or_name = sys.argv[1]
except IndexError as err:
    raise Exception('missing group id or name') from err

# experimental matcher for id shape as 5e1c5ec7-a634-4cd9-887a-618166d49a25
#                                      012345678
is_group_id = bool(UUID_PATTERN.match(group_id_or_name.lower()))
payload_key = 'groupId' if is_group_id else 'groupname'

query: QueryType = {
    'startAt': 0,
    payload_key: group_id_or_name,
    'includeInactiveUsers': True,
}

collector: CollectorType = {
    'endpoint': url,
    'query': {k: v for k, v in query.items() if k != 'startAt'},  # type: ignore
    'is_complete': False,
    'page_capacity': 0,
    'roundtrip_count': 0,
    'start_index': 0,
    'total_count': 0,
    'errors': [],
    'error_messages': [],
    'items': [],
}
my_start = 0
incomplete = True

while incomplete:
    query['startAt'] = my_start
    response = requests.request('GET', url, headers=headers, params=query, auth=auth)  # type: ignore
    data = json.loads(response.text)
    error_messages = data.get('errorMessages', [])
    if error_messages:
        for entry in error_messages:
            collector['error_messages'].append(entry)  # type: ignore
        errors = data.get('errors', [])
        for entry in errors:
            collector['errors'].append(entry)  # type: ignore
        break

    total = data['total']
    if not collector['total_count']:
        collector['total_count'] = total
    elif collector['total_count'] != total:
        raise IndexError(f'initial total_count({collector["total_count"]}) != ({total})')

    max_results = data['maxResults']
    if not collector['page_capacity']:
        collector['page_capacity'] = max_results
    elif collector['page_capacity'] != max_results:
        raise IndexError(f'initial page_capacity({collector["page_capacity"]}) != ({max_results})')

    for entry in data['values']:
        collector['items'].append(entry)  # type: ignore

    collector['is_complete'] = data['isLast']
    incomplete = not collector['is_complete']

    my_start += max_results
    collector['roundtrip_count'] += 1  # type: ignore


print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

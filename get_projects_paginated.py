#! /usr/bin/env python
"""GET - Get projects paginated.

Returns a paginated list of projects visible to the user.
This operation can be accessed anonymously.
Permissions required: Projects are returned only where the user has one of:

- Browse Projects project permission for the project.
- Administer Projects project permission for the project.
- Administer Jira global permission.

Data Security Policy: Not exempt from app access rules

## Scopes

Connect app scope required: READ
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:issue-type:jira, read:project:jira, read:project.property:jira,
    read:user:jira, read:application-role:jira, read:avatar:jira,
    read:group:jira, read:issue-type-hierarchy:jira, read:project-category:jira,
    read:project-version:jira, read:project.component:jira
"""
import json
import os
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

CollectorType = dict[str, Union[bool, int, str, list[object]]]

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/project/search'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query = {'startAt': 0}

collector: CollectorType = {
    'endpoint': url,
    'is_complete': False,
    'page_capacity': 0,
    'roundtrip_count': 0,
    'start_index': 0,
    'total_count': 0,
    'items': [],
}
my_start = 0
incomplete = True

while incomplete:
    query['startAt'] = my_start
    response = requests.request('GET', url, headers=headers, params=query, auth=auth)
    data = json.loads(response.text)

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

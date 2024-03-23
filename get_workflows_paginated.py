#! /usr/bin/env python
"""GET - Get workflows paginated.

Returns a paginated list of published classic workflows. When workflow names are specified, details of those workflows are returned. Otherwise, all published classic workflows are returned.

This operation does not return next-gen workflows.
Permissions required: Administer Jira global permission.
Data Security Policy: Exempt from app access rules

## Scopes

Connect app scope required: ADMIN
OAuth 2.0 scopes required:
Classic RECOMMENDED: manage:jira-project
Granular:
    read:group:jira, read:issue-security-level:jira, read:project-role:jira,
    read:screen:jira, read:status:jira, read:user:jira, read:workflow:jira,
    read:webhook:jira, read:avatar:jira, read:project-category:jira, read:project:jira

"""
import json
import os
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

CollectorType = dict[str, Union[bool, int, list[object]]]

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/workflow/search'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

collector: CollectorType = {
    'complete': False,
    'page_capacity': 0,
    'roundtrips': 0,
    'start_index': 0,
    'total_count': 0,
    'values': [],
}
my_start = 0
incomplete = True

while incomplete:
    my_url = f'{url}?startAt={my_start}'
    response = requests.request('GET', my_url, headers=headers, auth=auth)
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
        collector['values'].append(entry)  # type: ignore

    collector['complete'] = data['isLast']
    incomplete = not collector['complete']

    my_start += max_results
    collector['roundtrips'] += 1  # type: ignore


print(json.dumps(collector, sort_keys=True, indent=4, separators=(',', ': ')))

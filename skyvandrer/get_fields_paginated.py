#! /usr/bin/env python
"""Get fields paginated (of ticket management system).

Returns a paginated list of fields for Classic Jira projects. The list can include:

- all fields
- specific fields, by defining id
- fields that contain a string in the field name or description, by defining query
- specific fields that contain a string in the field name or description, by defining id and query

Only custom fields can be queried, type must be set to custom.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/#api-rest-api-3-field-search-get>

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

ENCODING = 'utf-8'

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/field/search'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query: QueryType = {'startAt': 0}

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

with open('fields.json', 'wt', encoding=ENCODING) as handle:
    json.dump(collector, handle, indent=2)

f_map = {}
for item in collector['items']:
    schema = item.get('schema', {})
    f_map[item['id']] = {
        'id': item['id'],
        'name': item['name'],
        'description': item['description'],
        'type': schema.get('type', None),
        'system': schema.get('system', None),
        'items': schema.get('items', None),
        'type': schema.get('type', None),
        'custom': schema.get('custom', None),
        'customId': schema.get('customId', 0),
    }

field_map = {key: f_map[key] for key in sorted(f_map)}
with open('field-map.json', 'wt', encoding=ENCODING) as handle:
    json.dump(field_map, handle, indent=2)

print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

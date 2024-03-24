#! /usr/bin/env python
"""Get screens (of ticket management system).

Returns a paginated list of all screens or those specified by one or more screen IDs.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-screens/#api-rest-api-3-screens-get>

"""
import json
import os
import re
import sys
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

url = f'{API_BASE_URL}/rest/api/3/screens'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

ci_query_string_or_scope = None
try:
    ci_query_string_or_scope = sys.argv[1]
except IndexError:
    pass

# experimental matcher for scopes having scope= in them
has_args = bool(ci_query_string_or_scope)
is_scope = bool(has_args and 'scope=' in ci_query_string_or_scope)  # type: ignore
payload_key = 'scope' if is_scope else 'queryString'

query: QueryType = {
    'startAt': 0,
    'orderBy': '+id',
    'scope': ['GLOBAL', 'PROJECT', 'TEMPLATE'],
}
if has_args:
    if is_scope:
        scope_values = [val.replace('scope=', '') for val in ci_query_string_or_scope.split(QUERY_SEP)]  # type: ignore
        query['scope'] = scope_values
    else:
        query['queryString'] = ci_query_string_or_scope  # type: ignore

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
    try:
        data = json.loads(response.text)
    except:  # noqa
        print(response.text)
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

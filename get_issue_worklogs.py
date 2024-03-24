#! /usr/bin/env python
"""Get issue worklogs (of ticket management system).

Returns worklogs for an issue, starting from the oldest worklog or from the worklog started on or after a date and time.
Time tracking must be enabled in Jira, otherwise this operation returns an error.
For more information, see Configuring time tracking.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/#api-rest-api-3-issue-issueidorkey-worklog-get>

"""

import json
import os
import sys
from typing import Union

import requests
from requests.auth import HTTPBasicAuth

CollectorType = dict[str, Union[bool, int, str, None, dict[str, str], list[object]]]
QueryType = dict[str, Union[int, str]]

API_BASE_URL = os.getenv('SUHTEITA_BASE_URL', '')
API_USER = os.getenv('SUHTEITA_USER', '')
API_TOKEN = os.getenv('SUHTEITA_TOKEN', '')

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

try:
    issue_id_or_key = sys.argv[1]
except IndexError as err:
    raise Exception('missing issue id or key') from err

url = f'{API_BASE_URL}/rest/api/3/issue/{issue_id_or_key}/worklog'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query: QueryType = {'startAt': 0}

collector: CollectorType = {
    'endpoint': url,
    'query': {k: v for k, v in query.items()},  # type: ignore
    'start_index': 0,
    'page_capacity': 0,
    'total_count': 0,
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
    for entry in data['worklogs']:
        collector['items'].append(entry)  # type: ignore

collector['page_capacity'] = data['maxResults']
collector['total_count'] = len(collector['items'])  # type: ignore

print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

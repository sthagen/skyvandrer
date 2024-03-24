#! /usr/bin/env python
"""Get issue (of ticket management system).

Returns the details for an issue.
The issue is identified by its ID or key, however, if the identifier doesn't match an issue,
a case-insensitive search and check for moved issues is performed.
If a matching issue is found its details are returned, a 302 or other redirect is not returned.
The issue key returned in the response is the key of the issue found.

Source:

<https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-issueidorkey-get>

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

url = f'{API_BASE_URL}/rest/api/3/issue/{issue_id_or_key}'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query: QueryType = {
    'fields': '*all',
    'fieldsByKeys': True,
    'expand': 'renderedFields,names,schema,transitions,editmeta,changelog,versionedRepresentations',
    'properties': '*all',
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
    collector['items'].append(data)  # type: ignore

collector['total_count'] = len(collector['items'])  # type: ignore

print(json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')))

#! /usr/bin/env python
"""GET - Search for filters.

Returns a paginated list of filters. Use this operation to get:

- specific filters, by defining id only.
- filters that match all of the specified attributes.
  For example, all filters for a user with a particular word in their name.
  When multiple attributes are specified only filters matching all attributes are returned.

This operation can be accessed anonymously.
Permissions required: None, however, only the following filters that match the query parameters are returned:

- filters owned by the user.
- filters shared with a group that the user is a member of.
- filters shared with a private project that the user has Browse projects project permission for.
- filters shared with a public project.
- filters shared with the public.

Data Security Policy: Not exempt from app access rules

## Scopes

Connect app scope required: READ
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:filter:jira, read:group:jira, read:project:jira, read:project-role:jira, read:user:jira,
    read:jql:jira, read:application-role:jira, read:avatar:jira, read:issue-type-hierarchy:jira

### Expansions

Use expand to include additional information about filter in the response. This parameter accepts a comma-separated list. Expand options include:

- `description` Returns the description of the filter.
- `favourite` Returns an indicator of whether the user has set the filter as a favorite.
- `favouritedCount` Returns a count of how many users have set this filter as a favorite.
- `jql` Returns the JQL query that the filter uses.
- `owner` Returns the owner of the filter.
- `searchUrl` Returns a URL to perform the filter's JQL query.
- `sharePermissions` Returns the share permissions defined for the filter.
- `editPermissions` Returns the edit permissions defined for the filter.
- `isWritable` Returns whether the current user has permission to edit the filter.
- `approximateLastUsed` [Experimental] Returns the approximate date and time when the filter was last evaluated.
- `subscriptions` Returns the users that are subscribed to the filter.
- `viewUrl` Returns a URL to view the filter.

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

COMMA = ','
EXPAND = COMMA.join(
    (
        'description',
        'owner',
        'jql',
        'viewUrl',
        'searchUrl',
        'favourite',
        'favouritedCount',
        'sharePermissions',
        'editPermissions',
        'isWritable',
        'approximateLastUsed',
        'subscriptions',
    )
)

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/filter/search'

auth = HTTPBasicAuth(API_USER, API_TOKEN)

headers = {'Accept': 'application/json'}

query = {
    'startAt': 0,
    'expand': EXPAND,
}

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
    response = requests.request('GET', url, headers=headers, params=query, auth=auth)  # type: ignore
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

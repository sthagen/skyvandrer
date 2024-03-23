#! /usr/bin/env python
"""GET - Search for dashboards.

Returns a paginated list of dashboards.
This operation is similar to Get dashboards except that the results can be refined to include dashboards that
have specific attributes. For example, dashboards with a particular name.
When multiple attributes are specified only filters matching all attributes are returned.
This operation can be accessed anonymously.
Permissions required: The following dashboards that match the query parameters are returned:

- Dashboards owned by the user. Not returned for anonymous users.
- Dashboards shared with a group that the user is a member of. Not returned for anonymous users.
- Dashboards shared with a private project that the user can browse. Not returned for anonymous users.
- Dashboards shared with a public project.
- Dashboards shared with the public.

Data Security Policy: Exempt from app access rules

## Scopes

Connect app scope required: READ
OAuth 2.0 scopes required:
Classic RECOMMENDED: read:jira-work
Granular:
    read:dashboard:jira, read:group:jira, read:project:jira, read:project-role:jira, read:user:jira,
    read:application-role:jira, read:avatar:jira, read:issue-type-hierarchy:jira, read:issue-type:jira,
    read:project-category:jira, read:project-version:jira, read:project.component:jira

### Expansions

Use expand to include additional information about dashboard in the response.
This parameter accepts a comma-separated list. Expand options include:

- `description` Returns the description of the dashboard.
- `owner` Returns the owner of the dashboard.
- `viewUrl` Returns the URL that is used to view the dashboard.
- `favourite` Returns isFavourite, an indicator of whether the user has set the dashboard as a favorite.
- `favouritedCount` Returns popularity, a count of how many users have set this dashboard as a favorite.
- `sharePermissions` Returns details of the share permissions defined for the dashboard.
- `editPermissions` Returns details of the edit permissions defined for the dashboard.
- `isWritable` Returns whether the current user has permission to edit the dashboard.

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
        'viewUrl',
        'favourite',
        'favouritedCount',
        'sharePermissions',
        'editPermissions',
        'isWritable',
    )
)

if not all(value for value in (API_BASE_URL, API_USER, API_TOKEN)):
    raise KeyError('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')

url = f'{API_BASE_URL}/rest/api/3/dashboard/search'

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

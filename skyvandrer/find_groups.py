"""Find groups (of ticket management system)."""

import json

import skyvandrer.rest as rest
from skyvandrer import API_BASE_URL, API_TOKEN, API_USER, CollectorType, QueryType, credentials_or_die


def find_groups(
    query_string: str, api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
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
    credentials_or_die(api_base_url=api_base_url, api_user=api_user, api_token=api_token)

    url = f'{API_BASE_URL}/rest/api/3/groups/picker'

    auth = rest.auth(api_user=api_user, api_token=api_token)

    headers = {'Accept': 'application/json'}

    query: QueryType = {
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

    response_text = rest.get(url, headers=headers, params=query, auth=auth)  # type: ignore
    data = json.loads(response_text)

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

    return collector

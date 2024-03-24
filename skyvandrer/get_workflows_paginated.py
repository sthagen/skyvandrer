"""Get workflows paginated (of ticket management system)."""

import json

import skyvandrer.rest as rest
from skyvandrer import API_BASE_URL, API_TOKEN, API_USER, CollectorType, QueryType, credentials_or_die


def get_workflows_paginated(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Get workflows paginated (of ticket management system).

    Returns a paginated list of published classic workflows. When workflow names are specified, details of those workflows are returned. Otherwise, all published classic workflows are returned.

    Source:

    <https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-workflows/#api-rest-api-3-workflow-search-get>
    """
    credentials_or_die(api_base_url=api_base_url, api_user=api_user, api_token=api_token)

    url = f'{API_BASE_URL}/rest/api/3/workflow/search'

    auth = rest.auth(api_user=api_user, api_token=api_token)

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
        response_text = rest.get(url, headers=headers, params=query, auth=auth)  # type: ignore
        data = json.loads(response_text)

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

    return collector

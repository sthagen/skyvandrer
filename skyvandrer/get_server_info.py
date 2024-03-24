"""Get ticket management system instance info."""

import json

import skyvandrer.rest as rest
from skyvandrer import API_BASE_URL, API_TOKEN, API_USER, CollectorType, QueryType, credentials_or_die


def get_server_info(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Get ticket management system instance info.

    Returns information about the Jira instance.

    Source:

    <https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-server-info/#api-rest-api-3-serverinfo-get>
    """
    credentials_or_die(api_base_url=api_base_url, api_user=api_user, api_token=api_token)

    url = f'{API_BASE_URL}/rest/api/3/serverInfo'

    auth = rest.auth(api_user=api_user, api_token=api_token)

    headers = {'Accept': 'application/json'}

    query: QueryType = {}

    collector: CollectorType = {
        'endpoint': url,
        'is_complete': False,
        'page_capacity': None,
        'roundtrip_count': 1,
        'offset': 0,
        'total_count': 0,
        'errors': [],
        'error_messages': [],
        'record': {},
    }
    response_text = rest.get(url, headers=headers, params=query, auth=auth)  # type: ignore
    data = json.loads(response_text)

    for k, v in data.items():
        collector['record'][k] = v  # type: ignore

    collector['total_count'] = len(collector['record'])  # type: ignore
    collector['is_complete'] = True

    return collector

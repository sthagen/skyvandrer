"""Get audit records (of ticket management system)."""

import json

import skyvandrer.rest as rest
from skyvandrer import API_BASE_URL, API_TOKEN, API_USER, CollectorType, QueryType, credentials_or_die


def get_audit_records(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Get audit records (of ticket management system).

    Returns a list of audit records. The list can be filtered to include items:
    - where each item in filter has at least one match in any of these fields:
      - summary
      - category
      - eventSource
      - objectItem.name If the object is a user, account ID is available to filter.
      - objectItem.parentName
      - objectItem.typeName
      - changedValues.changedFrom
      - changedValues.changedTo
      - remoteAddress

      For example, if filter contains man ed, an audit record containing summary":
      "User added to group" and "category": "group management" is returned.
      created on or after a date and time.
      created or or before a date and time.

    Source:

    <https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-audit-records/#api-rest-api-3-auditing-record-get>
    """
    credentials_or_die(api_base_url=api_base_url, api_user=api_user, api_token=api_token)

    url = f'{API_BASE_URL}/rest/api/3/auditing/record'

    auth = rest.auth(api_user=api_user, api_token=api_token)

    headers = {'Accept': 'application/json'}

    query: QueryType = {
        'offset': 0,
        'limit': 1000,
    }

    collector: CollectorType = {
        'endpoint': url,
        'is_complete': False,
        'page_capacity': query['limit'],  # type: ignore
        'roundtrip_count': 1,
        'offset': 0,
        'total_count': 0,
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
        collector['total_count'] = data.get('total', 0)
        for entry in data.get('records', []):
            collector['items'].append(entry)  # type: ignore

    collector['is_complete'] = True

    return collector

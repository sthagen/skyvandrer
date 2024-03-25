"""Cloud Walker (Norwegian: skyvandrer) - application programming interface."""

from requests.auth import HTTPBasicAuth

from skyvandrer import API_BASE_URL, API_TOKEN, API_USER, CollectorType
from skyvandrer.fetch import fetch_issues as impl_fetch_issues
from skyvandrer.fetch import WAIT_MAX_MILLIS
from skyvandrer.find_groups import find_groups as impl_find_groups
from skyvandrer.get_audit_records import get_audit_records as impl_get_audit_records
from skyvandrer.get_server_info import get_server_info as impl_get_server_info
from skyvandrer.get_workflows_paginated import get_workflows_paginated as impl_get_workflows_paginated
from skyvandrer.search_for_dashboards import search_for_dashboards as impl_search_for_dashboards
from skyvandrer.search_for_filters import search_for_filters as impl_search_for_filters
from skyvandrer.search_priorities import search_priorities as impl_search_priorities


def fetch_issues(args: list[str], auth_token: HTTPBasicAuth, wait_max_millis: float = WAIT_MAX_MILLIS) -> None:
    """Proxy to fetch-issues/3 implementation."""
    return impl_fetch_issues(args, auth_token=auth_token, wait_max_millis=wait_max_millis)


def find_groups(
    query_string: str, api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Proxy to find-groups/1 implementation."""
    return impl_find_groups(query_string, api_base_url=api_base_url, api_user=api_user, api_token=api_token)


def get_audit_records(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Proxy to get-audit-records/0 implementation."""
    return impl_get_audit_records(api_base_url=api_base_url, api_user=api_user, api_token=api_token)


def get_server_info(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Proxy to get-server-info/0 implementation."""
    return impl_get_server_info(api_base_url=api_base_url, api_user=api_user, api_token=api_token)


def get_workflows_paginated(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Proxy to get-workflows-paginated/0 implementation."""
    return impl_get_workflows_paginated(api_base_url=api_base_url, api_user=api_user, api_token=api_token)


def search_for_dashboards(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Proxy to search-for-dashboards/0 implementation."""
    return impl_search_for_dashboards(api_base_url=api_base_url, api_user=api_user, api_token=api_token)


def search_for_filters(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Proxy to search-for-filters/0 implementation."""
    return impl_search_for_filters(api_base_url=api_base_url, api_user=api_user, api_token=api_token)


def search_priorities(
    api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN
) -> CollectorType:
    """Proxy to search-priorities/0 implementation."""
    return impl_search_priorities(api_base_url=api_base_url, api_user=api_user, api_token=api_token)

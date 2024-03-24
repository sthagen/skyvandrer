"""Cloud Walker (Norwegian: skyvandrer) - application programming interface."""

from skyvandrer import API_BASE_URL, API_TOKEN, API_USER, CollectorType
from skyvandrer.find_groups import find_groups as impl_find_groups
from skyvandrer.get_audit_records import get_audit_records as impl_get_audit_records


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

"""Cloud Walker (Norwegian: skyvandrer) - REST interface."""

import requests
from requests.auth import HTTPBasicAuth
from skyvandrer import API_TOKEN, API_USER, QueryType, log


def invoke(http_verb: str, url: str, headers: dict[str, str], params: QueryType, auth: str) -> str:
    """DRY."""
    log.info(f'{http_verb=}')
    log.info(f'{url=}')
    log.info(f'{headers=}')
    log.info(f'{params=}')
    log.info(f'{auth=}')
    response = requests.request(http_verb, url, headers=headers, params=params, auth=auth)  # type: ignore
    return response.text


def get(url: str, headers: dict[str, str], params: QueryType, auth: str) -> str:
    """DRY."""
    return invoke('GET', url, headers=headers, params=params, auth=auth)  # type: ignore


def auth(api_user: str = API_USER, api_token: str = API_TOKEN) -> HTTPBasicAuth:
    """DRY."""
    return HTTPBasicAuth(API_USER, API_TOKEN)

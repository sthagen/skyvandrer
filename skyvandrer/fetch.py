"""Fetch a thing or two from the nineties."""

import datetime as dti
import json
import lzma
import os
import pathlib
import random
import time
from typing import Union, no_type_check

import requests
from requests.auth import HTTPBasicAuth

from skyvandrer import API_BASE_URL, DASH, DEBUG, ENCODING, ENCODING_ERRORS_POLICY, ISSUE_STORAGE, log, parse_timestamp

ISSUE_API_ROOT = '/rest/api/latest/issue/'
ISSUE_ACTION = '?expand=changelog'
ISSUE_URL_TEMPLATE = API_BASE_URL + ISSUE_API_ROOT + "%s" + ISSUE_ACTION

XZ_FILTERS = [{'id': lzma.FILTER_LZMA2, 'preset': 7 | lzma.PRESET_EXTREME}]
XZ_EXT = '.xz'

WAIT_MAX_MILLIS = 1.0e3

# Non-existing ticket:
# {"errorMessages":["Issue Does Not Exist"],"errors":{}}
CHECK = 'errorMessages'


@no_type_check
def has_data(issue: dict[str, object]) -> bool:
    """DRY."""
    return issue and CHECK not in issue


@no_type_check
def archive(data, file_path: pathlib.Path) -> None:
    """Create .xz files for long term storage."""
    if file_path.suffixes[-1] != XZ_EXT:
        file_path = file_path.with_suffix(file_path.suffix + XZ_EXT)
    with lzma.open(file_path, 'w', check=lzma.CHECK_SHA256, filters=XZ_FILTERS) as f:
        f.write(json.dumps(data).encode(encoding=ENCODING, errors=ENCODING_ERRORS_POLICY))


def looks_like_issue_key(a_key: str) -> bool:
    """Some minimal guard against useless (non-existing) issue dumps."""
    if not a_key:
        return False
    project, serial = a_key.split(DASH, 1)
    if not project or not serial:
        return False
    if any(not c.isupper() for c in project):
        return False
    if any(not c.isdigit() for c in serial):
        return False
    return True


@no_type_check
def valid_update_timestamp(data: dict[str, object]) -> Union[str, None]:
    """Attempt safe extract and parse of updated issue timestamp."""
    fields = data.get('fields')
    if fields:
        updated_string = fields.get('updated')
        if updated_string:
            return parse_timestamp(updated_string)
    return None


@no_type_check
def fetch_issue(issue_key: str, auth_token: HTTPBasicAuth, wait_max_millis: float = WAIT_MAX_MILLIS) -> None:
    """DRY."""
    millis = random.uniform(0.0, wait_max_millis)
    time.sleep(millis / 1e3)
    log.debug(
        f'  at({dti.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")}), nice({millis / 1e3 :5.3f})secs, then({issue_key}) ...'
    )
    headers = {'Content-Type': 'application/json'}
    project = issue_key.split(DASH, 1)[0].lower()
    project_path = pathlib.Path(ISSUE_STORAGE, project)
    project_path.mkdir(parents=True, exist_ok=True)
    r = requests.get(
        ISSUE_URL_TEMPLATE % (issue_key,),
        auth=auth_token,
        headers=headers,
    )
    data = r.json()
    if DEBUG:
        with open(f'{issue_key.lower()}.json', 'w') as dump:
            json.dump(data, dump)
    if has_data(data):
        archive_file_path = project_path / f'{issue_key.lower()}.json{XZ_EXT}'
        archive(data, archive_file_path)
        archived_size = archive_file_path.stat().st_size
        log.debug(f'{archived_size :10d} <- ({r.status_code}, {r.encoding}, {len(r.content)} bytes)')
        updated = valid_update_timestamp(data)
        if updated:
            a_time = time.mktime(updated.timetuple())
            m_time = a_time
            os.utime(archive_file_path, (a_time, m_time))
        else:
            log.error(f'failed updated timestamp extraction for {issue_key}')


@no_type_check
def fetch_issues(args: list[str], auth_token: HTTPBasicAuth, wait_max_millis: float = WAIT_MAX_MILLIS) -> None:
    """Fetch and inspect."""
    if not args:
        raise ValueError(f'nothing to pull in args ({args})?')
    random.seed(time.time_ns())
    for a_key in args:
        if looks_like_issue_key(a_key):
            fetch_issue(a_key, auth_token=auth_token, wait_max_millis=wait_max_millis)
        else:
            log.debug(f'ignoring possibly invalid issue key ({a_key})')
    log.info(f'that is all for now and args ({args})')

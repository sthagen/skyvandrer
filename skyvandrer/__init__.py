"""Cloud Walker (Norwegian: skyvandrer) - Exploring a historic REST interface."""

import datetime as dti
import logging
import operator
import os
import pathlib
from typing import Union, no_type_check

# [[[fill git_describe()]]]
__version__ = '2024.3.25+parent.abadcafe'
# [[[end]]]
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)

APP_ALIAS = str(pathlib.Path(__file__).parent.name)
APP_ENV = APP_ALIAS.upper()
APP_NAME = locals()['__doc__']
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
QUIET = False
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = f'.{APP_ALIAS}.json'
DEFAULT_LF_ONLY = 'YES'
log = logging.getLogger()  # Module level logger is sufficient
LOG_FOLDER = pathlib.Path('logs')
LOG_FILE = f'{APP_ALIAS}.log'
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO
VERSION = __version__
VERSION_DOTTED_TRIPLE = '.'.join(__version_info__[:3])
TS_FORMAT_LOG = '%Y-%m-%dT%H:%M:%S'
TS_FORMAT_PAYLOADS = '%Y-%m-%d %H:%M:%S.%f UTC'
TS_FORMAT_GENERATOR = '%Y-%m-%d %H:%M:%S.%f +00:00'

API_BASE_URL = os.getenv(f'{APP_ENV}_BASE_URL', '')
API_USER = os.getenv(f'{APP_ENV}_USER', '')
API_TOKEN = os.getenv(f'{APP_ENV}_TOKEN', '')

NL = '\n'

DASH = '-'
ISO_FMT = '%Y-%m-%dT%H:%M:%S.%f'
ISO_LENGTH = len('YYYY-mm-ddTHH:MM:SS.fff')
TZ_OP = {'+': operator.sub, '-': operator.add}  # + indicates ahead of UTC

JR_NULL = '<null>'
NA = 'n/a'

REL_ISSUE_STORAGE = "issue"
ISSUE_STORAGE_DEFAULT = pathlib.Path(pathlib.Path.home(), "d", "ticket-management-system-analysis", REL_ISSUE_STORAGE)
ISSUE_STORAGE_ENV = os.getenv(f'{APP_ENV}_ISSUE_STORAGE', '')

ISSUE_STORAGE = pathlib.Path(ISSUE_STORAGE_ENV).expanduser().resolve() if ISSUE_STORAGE_ENV else ISSUE_STORAGE_DEFAULT


CollectorType = dict[str, Union[bool, int, str, None, dict[str, str], list[object]]]
QueryType = dict[str, Union[bool, int, str, list[str]]]

__all__: list[str] = [
    'API_BASE_URL',
    'API_TOKEN',
    'API_USER',
    'APP_ALIAS',
    'APP_ENV',
    'APP_NAME',
    'DEBUG',
    'DEFAULT_CONFIG_NAME',
    'ENCODING',
    'TS_FORMAT_GENERATOR',
    'VERSION',
    'VERSION_DOTTED_TRIPLE',
    'CollectorType',
    'QueryType',
    'log',
]


def credentials_or_die(api_base_url: str = API_BASE_URL, api_user: str = API_USER, api_token: str = API_TOKEN) -> bool:
    """Verify the credentials given are plausible (For now, truthy suffices.)"""
    if not all(value for value in (api_base_url, api_user, api_token)):
        log.fatal('missing at least one value for API_BASE_URL, API_USER, and API_TOKEN')
    return True


def split_at(text_fragment: str, pos: int) -> tuple[str, str]:
    """Split text fragment by position and return pair as tuple."""
    return text_fragment[:pos], text_fragment[pos:]


@no_type_check
def parse_timestamp(text_stamp: str, iso_fmt: str = ISO_FMT) -> str:
    """
    Parse the timestamp formats found in REST responses from the Nineties.

    Return as datetime timestamp in UTC (implicit).
    """
    if text_stamp is None or text_stamp == JR_NULL:
        return None

    iso_value, off = split_at(text_stamp, ISO_LENGTH)
    local_time = dti.datetime.strptime(iso_value, iso_fmt)
    if not off:
        return local_time

    sign_pos = 0
    assert off and off[sign_pos] in TZ_OP  # nosec B101

    m_start = 3 if ':' not in off else 4
    assert len(off) == m_start + 2  # nosec B101

    oper, hours, minutes = off[sign_pos], int(off[1:3]), int(off[m_start:])

    return TZ_OP[oper](local_time, dti.timedelta(hours=hours, minutes=minutes))


@no_type_check
def formatTime_RFC3339(self, record, datefmt=None):  # noqa
    """HACK A DID ACK we could inject .astimezone() to localize ..."""
    return dti.datetime.fromtimestamp(record.created, dti.timezone.utc).isoformat()  # pragma: no cover


@no_type_check
def init_logger(name=None, level=None):
    """Initialize module level logger"""
    global log  # pylint: disable=global-statement

    log_format = {
        'format': '%(asctime)s %(levelname)s [%(name)s]: %(message)s',
        'datefmt': TS_FORMAT_LOG,
        # 'filename': LOG_PATH,
        'level': LOG_LEVEL if level is None else level,
    }
    logging.Formatter.formatTime = formatTime_RFC3339
    logging.basicConfig(**log_format)
    log = logging.getLogger(APP_ENV if name is None else name)
    log.propagate = True


init_logger(name=APP_ALIAS, level=logging.DEBUG if DEBUG else None)

"""Cloud Walker (Norwegian: skyvandrer) - Exploring a historic REST interface."""

import datetime as dti
import logging
import os
import pathlib
from typing import Union, no_type_check

# [[[fill git_describe()]]]
__version__ = '2023.11.29+parent.g53f523fd'
# [[[end]]] (checksum: a851508854340075dd2880298dc6133b)
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

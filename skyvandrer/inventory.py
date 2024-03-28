"""Inventory of proxy."""
import datetime as dti
import hashlib
import json
import lzma
import pathlib
import sys
from typing import Union, no_type_check

PathlikeType = Union[str, pathlib.Path]

CHUNK_SIZE = 2 << 15
DASH = '-'
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
ISO_FMT = '%Y-%m-%dT%H:%M:%S+00:00'
XZ_EXT = '.xz'
XZ_FILTERS = [{'id': lzma.FILTER_LZMA2, 'preset': 7 | lzma.PRESET_EXTREME}]
LZMA_KWARGS = {'check': lzma.CHECK_SHA256, 'filters': XZ_FILTERS}
SECONDS_PER_DAY = 86_400

HASHER = {
    'sha512': hashlib.sha512,
    'sha256': hashlib.sha256,
}


def file_stats(path: PathlikeType) -> tuple[int, dti.datetime, dti.datetime]:
    """File system stats of file."""
    stats = pathlib.Path(path).stat()
    return stats.st_size, stats.st_mtime, stats.st_atime


def hash_file(path: PathlikeType, algo: str = 'sha256') -> str:
    """Return the SHA256 hex digest of the data from file."""
    if algo not in HASHER:
        raise KeyError(f'Unsupported hash algorithm requested - {algo} is not in {tuple(HASHER.keys())}')
    hash = HASHER[algo]()
    with open(path, 'rb') as handle:
        while chunk := handle.read(CHUNK_SIZE):
            hash.update(chunk)
    return hash.hexdigest()


def key_id_from_path(path: PathlikeType) -> tuple[str, int]:
    """Extract (project) code identifying number from path."""
    a_path = pathlib.Path(path)
    suffixes = a_path.suffixes
    a_key = a_path.name
    for suffix in suffixes:
        a_key = a_key.replace(suffix, '')
    code, serial = a_key.upper().split(DASH)
    return code, int(serial)


collector = {}
max_serial = 0
the_code = None
the_container_path = None
for path in sys.argv[1:]:
    fingerprint = hash_file(path)
    size_bytes, m_time, a_time = file_stats(path)
    m_ts_disp = dti.datetime.utcfromtimestamp(m_time).strftime(ISO_FMT)
    code, serial = key_id_from_path(path)

    if the_code is None:
        the_code = code
    elif the_code != code:
        raise ValueError('do not mix dfferent projects to inventize')

    if the_container_path is None:
        the_container_path = str(pathlib.Path(path).parent)
    elif the_container_path != str(pathlib.Path(path).parent):
        raise ValueError('do not mix projects from different containers')

    max_serial = max(serial, max_serial)
    key = f'{code}-{serial}'
    collector[key] = {
        'path': str(path),
        'code': code,
        'serial': serial,
        'size_bytes_compresed': size_bytes,
        'modified': m_ts_disp,
        'fingerprint': f'sha256:{fingerprint}'
    }
    print(f'{code}-{serial} <- ({size_bytes} bytes, modified:{m_ts_disp}, sha256:{fingerprint})')

inventory = {}
project_stats = {
    the_code: {
        'container_path': the_container_path,
        'sum_size_bytes_compressed': 0,
        'min_size_bytes_compressed': 999_999_999_999,
        'max_size_bytes_compressed': 0,
        'min_modified': '9999-12-31T23:59:59+00:00',
        'max_modified': '1111-01-01T00:00:00+00:00',
        'timespan_modified_seconds': 0,
        'timespan_modified_days': 0,
        'min_serial': 999_999,
        'max_serial': 0,
        'nominal_issue_count': 0,
        'found_issue_count': 0,
        'missing_issue_count': 0,
        'issue_defect_rate': 0,
    }
}
min_size = project_stats[the_code]['min_size_bytes_compressed']
max_size = project_stats[the_code]['max_size_bytes_compressed']
min_modified = project_stats[the_code]['min_modified']
max_modified = project_stats[the_code]['max_modified']
min_serial = project_stats[the_code]['min_serial']
for serial in range(1, max_serial + 1):
    project_stats[the_code]['nominal_issue_count'] += 1
    key = f'{the_code}-{serial}'
    if key in collector:
        project_stats[the_code]['found_issue_count'] += 1
        project_stats[the_code]['sum_size_bytes_compressed'] += collector[key]['size_bytes_compresed']
        min_size = min(min_size, collector[key]['size_bytes_compresed'])
        max_size = max(max_size, collector[key]['size_bytes_compresed'])
        min_modified = min(min_modified, collector[key]['modified'])
        max_modified = max(max_modified, collector[key]['modified'])
        min_serial = min(min_serial, serial)
        inventory[key] = collector[key]
    else:
        inventory[key] = {}

project_stats[the_code]['min_size_bytes_compressed'] = min_size
project_stats[the_code]['max_size_bytes_compressed'] = max_size

project_stats[the_code]['min_modified'] = min_modified
project_stats[the_code]['max_modified'] = max_modified
timespan_seconds = (dti.datetime.strptime(max_modified, ISO_FMT) - dti.datetime.strptime(min_modified, ISO_FMT)).total_seconds()
project_stats[the_code]['timespan_modified_seconds'] = timespan_seconds
project_stats[the_code]['timespan_modified_days'] = timespan_seconds / SECONDS_PER_DAY

project_stats[the_code]['min_serial'] = min_serial
project_stats[the_code]['max_serial'] = max_serial

project_stats[the_code]['missing_issue_count'] = project_stats[the_code]['nominal_issue_count'] - project_stats[the_code]['found_issue_count']
project_stats[the_code]['issue_defect_rate'] = project_stats[the_code]['missing_issue_count'] / project_stats[the_code]['nominal_issue_count']

print(json.dumps(project_stats, indent=2))
with open(f'inventory/{the_code.lower()}.json', 'wt', encoding=ENCODING) as handle:
    json.dump(inventory, handle, indent=2)

with open(f'inventory/index.json', 'rt', encoding=ENCODING) as handle:
    index = json.load(handle)

index[the_code] = project_stats[the_code]

with open(f'inventory/index.json', 'wt', encoding=ENCODING) as handle:
    json.dump(index, handle, indent=2)

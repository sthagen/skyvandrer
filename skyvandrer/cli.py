"""Cloud Walker (Norwegian: skyvandrer) - command line interface."""

import json
import sys
from typing import Union

from skyvandrer import APP_ALIAS, NL, CollectorType, log
import skyvandrer.api as api


def log_collector(collector: CollectorType) -> None:
    """DRY."""
    for line in json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')).split(NL):
        log.info(line)


def reduce_args(args: list[str], task: str) -> list[str]:
    """Remove the task from the arguments list."""
    args = [arg for arg in args if arg != task]
    log.debug(args)
    return args


def app(args: Union[None, list[str]], prog_name: str = APP_ALIAS) -> int:
    """DRY."""
    if args is None:
        args = sys.argv[1:]

    task = 'find-groups'
    if task in args:
        args = reduce_args(args, task)
        try:
            query_string = args[0]
        except IndexError as err:
            message = 'missing query string'
            log.fatal(message)
            raise Exception(message) from err

        log_collector(api.find_groups(query_string))
        return 0

    task = 'get-audit-records'
    if task in args:
        log_collector(api.get_audit_records())
        return 0

    task = 'get-server-info'
    if task in args:
        args = reduce_args(args, task)
        return 0

    task = 'get-workflows-paginated'
    if task in args:
        log_collector(api.get_workflows_paginated())
        return 0

    task = 'search-for-filters'
    if task in args:
        log_collector(api.search_for_filters())
        return 0

    return 1

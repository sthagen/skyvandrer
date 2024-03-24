"""Cloud Walker (Norwegian: skyvandrer) - command line interface."""

import json
import sys
from typing import Union

from skyvandrer import APP_ALIAS, NL, log
import skyvandrer.api as api


def app(args: Union[None, list[str]], prog_name: str = APP_ALIAS) -> int:
    """DRY."""
    if args is None:
        args = sys.argv[1:]

    task = 'find-groups'
    if task in args:
        args = [arg for arg in args if arg != task]
        log.debug(args)
        try:
            query_string = args[0]
        except IndexError as err:
            message = 'missing query string'
            log.fatal(message)
            raise Exception(message) from err

        collector = api.find_groups(query_string)
        for line in json.dumps(collector, sort_keys=False, indent=4, separators=(',', ': ')).split(NL):
            log.info(line)
        return 0
    return 1

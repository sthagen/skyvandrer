import sys

from skyvandrer.cli import app
from skyvandrer import APP_ALIAS

if __name__ == '__main__':
    sys.exit(app(args=sys.argv[1:], prog_name=APP_ALIAS))  # pragma: no cover

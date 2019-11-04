import logging

from example.core import KedroCore

logging.basicConfig(level='DEBUG')


kedro = KedroCore()
kedro.run_cli()

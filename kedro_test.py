import logging

from example.core import KedroCore

logging.basicConfig(level='INFO')


kedro = KedroCore()
kedro.run_cli()

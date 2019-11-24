from example.cli import KedroCLIAspect
from example.cli_plugin import CLIPluginAspect
from example.config_loader import ConfigLoaderAspect
from example.workflows import WorkflowAspect
from pointcut import PointcutDispatcher



class KedroCore:
    def __init__(self):
        self._dispatcher = PointcutDispatcher([
            ConfigLoaderAspect,
            WorkflowAspect,
            KedroCLIAspect,
            CLIPluginAspect,


            RestApiAspect,
            # JournalingAspect,
            # PAIAspect,
            # KedroViz,
        ])

    def run_cli(self):
        self._dispatcher.send('kedro_cli.run_cli')

    def run(self, *args, **kwargs):
        self._dispatcher.send('runner.run_pipeline')

    @property
    def catalog(self):
        return self._dispatcher.send('catalog_loader.load')


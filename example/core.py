from example.cli import KedroCLIAspect
from example.context import ContextAspect
from pointcut import PointcutDispatcher, Aspect, delegate, multi_delegate



class KedroCoreAspect(Aspect):
    pass


class KedroCore:
    def __init__(self):
        self._dispatcher = PointcutDispatcher([
            KedroCore,
            KedroCLIAspect,
            ContextAspect,
        ])

    def run_cli(self):
        self._dispatcher.send('kedro_cli.run_cli')

    def run(self, *args, **kwargs):
        self._dispatcher.send('')

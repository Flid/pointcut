from typing import List, Any

import click

from example.runner import RunnerAspect
from pointcut import Aspect, multi_delegate, delegate


class KedroCLIAspect(RunnerAspect):
    NAMESPACE = 'kedro_cli'

    @multi_delegate()
    def collect_cli_commands(cls) -> List[Any]:
        @click.option(
            "--host",
            default="127.0.0.1",
            help="Host that viz will listen to. Defaults to 127.0.0.1.",
        )
        def some_command(host):
            print('Doing something useful...')

        def run():
            result = cls.run_pipeline()
            print('Pipeline run result', result)

        return [
            {
                'args': {
                    'context_settings': {'help_option_names': ["-h", "--help"]},
                },
                'func': some_command,
            },
            {
                'args': {},
                'func': run,
            }
        ]

    @delegate()
    def build_cli_interface(cls):
        commands = cls.collect_cli_commands()

        commands_flat = []
        for aspect_group in commands:
            commands_flat += aspect_group

        return commands_flat

    @delegate()
    def run_cli(cls):

        @click.group(name="Kedro")
        def commands():
            pass

        cli_commands = cls.build_cli_interface()

        for cli_command in cli_commands:
            commands.command(**cli_command['args'])(cli_command['func'])

        commands()

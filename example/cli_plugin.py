from typing import List, Any

from pointcut import Aspect, add_multi_delegate, overwrite_delegate


class CLIPluginAspect(Aspect):
    NAMESPACE = 'kedro_cli'

    @add_multi_delegate()
    def collect_cli_commands(cls) -> List[Any]:
        def plugin_stuff():
            print('Doing the pluginish stuff...')

        return [
            {
                'args': {},
                'func': plugin_stuff,
            },
        ]

    @overwrite_delegate(namespace='config_loader')
    def parse_content(cls, raw_content_dict):
        print('CUSTOM CONFIG PARSER!')
        return raw_content_dict

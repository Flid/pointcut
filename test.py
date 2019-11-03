from typing import List, Dict

from pointcut import Aspect, PointcutDispatcher, delegate, overwrite_delegate
import logging


logging.basicConfig(level='INFO')


class ConfigLoadAspect(Aspect):
    NAMESPACE = "config_loader"

    @delegate()
    def load_config(self):
        raw_content_dict = self.get_content()
        content_dict = self.parse_content(raw_content_dict)
        return content_dict

    @delegate()
    def get_content(self):
        return {"raw": "content"}

    @delegate()
    def parse_content(self, raw_content_dict):
        return raw_content_dict


class LoadConfigMultiFileStrategy(ConfigLoadAspect):
    @overwrite_delegate()
    def get_content(self):
        sources = self.get_content_sources()

        contents = []

        for source in sources:
            contents.append(self.load_content_source(source))

        return self.merge_content(contents)

    @delegate()
    def get_content_sources(self):
        return []

    @delegate()
    def load_content_source(self, content_source):
        return {}

    @delegate()
    def merge_content(self, content_list: List[Dict]):
        output = {}
        for conf_dict in content_list:
            output.update(conf_dict)

        return output


class LocalConfigLoader(LoadConfigMultiFileStrategy):
    @overwrite_delegate()
    def get_content_sources(self):
        return ["source1", "source2"]

    @overwrite_delegate()
    def load_content_source(self, content_source):
        return {content_source: "some data"}


class TemplatedConfigAspect(Aspect):
    NAMESPACE = 'config_loader'

    @overwrite_delegate()
    def parse_content(self, raw_content_dict):
        return {'parsed': raw_content_dict}


class RemoteConfigAspect(Aspect):
    NAMESPACE = 'config_loader'

    @overwrite_delegate()
    def load_content_source(self, content_source):
        return {content_source: 'remote stuff'}

    @overwrite_delegate()
    def collect_cli_commands(self):
        return [

        ]


print(LocalConfigLoader().load_config())
print('Now with dispatcher')


core = PointcutDispatcher([
    LocalConfigLoader,
    #TemplatedConfigAspect,
    #RemoteConfigAspect,
])
print(core.send("config_loader.load_config"))

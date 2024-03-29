from typing import List, Dict

from pointcut import Aspect, PointcutDispatcher, delegate, overwrite_delegate, multi_delegate, add_multi_delegate
import logging


logging.basicConfig(level='DEBUG')


class ConfigLoadAspect(Aspect):
    NAMESPACE = "config_loader"

    @delegate()
    def load_config(cls):
        raw_content_dict = cls.get_content()
        content_dict = cls.parse_content(raw_content_dict)
        return content_dict

    @delegate()
    def get_content(cls):
        return {"raw": "content"}

    @delegate()
    def parse_content(cls, raw_content_dict):
        return raw_content_dict


class LoadConfigMultiFileStrategy(ConfigLoadAspect):
    @overwrite_delegate()
    def get_content(cls):
        sources = cls.get_content_sources()

        contents = []

        for source in sources:
            contents.append(cls.load_content_source(source))

        return cls.merge_content(contents)

    @delegate()
    def get_content_sources(cls):
        return []

    @delegate()
    def load_content_source(cls, content_source):
        return {}

    @delegate()
    def merge_content(cls, content_list: List[Dict]):
        output = {}
        for conf_dict in content_list:
            output.update(conf_dict)

        return output


class LocalConfigLoader(LoadConfigMultiFileStrategy):
    @overwrite_delegate()
    def get_content_sources(cls):
        return ["source1", "source2"]

    @overwrite_delegate()
    def load_content_source(cls, content_source):
        return {content_source: "some data"}


class TemplatedConfigAspect(LoadConfigMultiFileStrategy):
    NAMESPACE = 'config_loader'

    @overwrite_delegate()
    def parse_content(cls, raw_content_dict):
        return {'parsed': raw_content_dict}


class RemoteConfigAspect(LoadConfigMultiFileStrategy):
    NAMESPACE = 'config_loader'

    @overwrite_delegate()
    def load_content_source(cls, content_source):
        return {content_source: 'remote stuff'}


# You can run it just instantiating the class
print(LocalConfigLoader().load_config())


# But the real power comes with the dispatcher:
core = PointcutDispatcher([
    LocalConfigLoader,
    TemplatedConfigAspect,
    RemoteConfigAspect,
])
print(core.send("config_loader.load_config"))


"""
* Control over inheritance
* Many types of delegates
* No "event dispatching" around the code, looks like function calls
* Free pre/post events
* Ability to dynamically add/remove aspects
"""

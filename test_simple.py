from typing import List, Dict
import logging


logging.basicConfig(level='DEBUG')


class ConfigLoadAspect:
    @classmethod
    def load_config(cls):
        raw_content_dict = cls.get_content()
        content_dict = cls.parse_content(raw_content_dict)
        return content_dict

    @classmethod
    def get_content(cls):
        return {"raw": "content"}

    @classmethod
    def parse_content(cls, raw_content_dict):
        return raw_content_dict


class LoadConfigMultiFileStrategy(ConfigLoadAspect):
    @classmethod
    def get_content(cls):
        sources = cls.get_content_sources()

        contents = []

        for source in sources:
            contents.append(cls.load_content_source(source))

        return cls.merge_content(contents)

    @classmethod
    def get_content_sources(cls):
        return []

    @classmethod
    def load_content_source(cls, content_source):
        return {}

    @classmethod
    def merge_content(cls, content_list: List[Dict]):
        output = {}
        for conf_dict in content_list:
            output.update(conf_dict)

        return output


class LocalConfigLoader(LoadConfigMultiFileStrategy):
    @classmethod
    def get_content_sources(cls):
        return ["source1", "source2"]

    @classmethod
    def load_content_source(cls, content_source):
        return {content_source: "some data"}


class TemplatedConfigAspect(LoadConfigMultiFileStrategy):
    @classmethod
    def parse_content(cls, raw_content_dict):
        return {'parsed': raw_content_dict}


class RemoteConfigAspect(LoadConfigMultiFileStrategy):
    @classmethod
    def load_content_source(cls, content_source):
        return {content_source: 'remote stuff'}



class UserDefinedConfigLoader(RemoteConfigAspect, TemplatedConfigAspect, LocalConfigLoader):
    pass


print(UserDefinedConfigLoader().load_config())


"""
Cons:
* Not OOP
* Name clashing
* The final class looks messy
* Multiple function overrides might clash


Pros:
* Extend anything anywhere
* New functionality comes completely isolated, injected to the system
* Clear functionality dependencies through class inheritance
* Easy to test
* The structure is messy, but it can be visualized, statically analysed.
"""

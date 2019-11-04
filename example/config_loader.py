from pointcut import Aspect, delegate


class ConfigData:
    def __init__(self, config_dict):
        self.config_dict = config_dict


class ConfigLoaderAspect(Aspect):
    NAMESPACE = 'config_loader'

    @delegate()
    def retrieve_content(cls, search_args):
        return {
            'key': 'value',
            'search_args': search_args,
        }

    @delegate()
    def parse_content(cls, raw_content_dict):
        return raw_content_dict

    @delegate()
    def make_config_dict(cls, content_dict):
        return ConfigData(content_dict)

    @delegate()
    def load_config(cls, search_args):
        raw_content_dict = cls.retrieve_content(search_args=search_args)
        content_dict = cls.parse_content(raw_content_dict=raw_content_dict)
        return cls.make_config_dict(content_dict=content_dict)

from example.catalog import CatalogAspect
from example.config_loader import ConfigLoaderAspect
from pointcut import Aspect, delegate


class RunnerData:
    def __init__(self, num_workers, config_data, catalog_data):
        self.num_workers = num_workers
        self.config_data = config_data
        self.catalog_data = catalog_data


class RunnerAspect(ConfigLoaderAspect, CatalogAspect):
    NAMESPACE = 'runner'

    @delegate()
    def init_runner(cls, num_workers=1) -> RunnerData:
        return RunnerData(
            config_data=cls.load_config(search_args='whatever'),
            catalog_data=cls.load_catalog(),
            num_workers=num_workers,
        )

    @delegate()
    def run_pipeline(cls, runner_data, pipeline):
        print('Running pipeline', pipeline, runner_data)
        return {'pipeline': 'result'}

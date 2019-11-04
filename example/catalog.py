from pointcut import Aspect, delegate


class CatalogData:
    def __init__(self, datasets):
        self.datasets = datasets


class CatalogAspect(Aspect):
    NAMESPACE = 'catalog'

    @delegate()
    def load_catalog(cls):
        # NOTE - very basic, can be split just like ConfigAspect
        return CatalogData(datasets=['dataset1', 'dataset2'])

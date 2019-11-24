import logging

logger = logging.getLogger(__name__)


class DelegateBase:
    def __init__(self, namespace=None):
        self._overwrite_namespace = namespace
        self._func = None
        self._dispatcher = None
        self._aspect = None
        self._origin_aspect_cls = None

    def _bootstrap_dispatcher(self, dispatcher):
        self._dispatcher = dispatcher

    def _bootstrap_aspect(self, aspect, origin_aspect_cls):
        self._aspect = aspect
        self._origin_aspect_cls = origin_aspect_cls

    @property
    def name(self):
        if not self._origin_aspect_cls.NAMESPACE:
            raise ValueError('Aspect {} has no namespace'.format(self._origin_aspect_cls))

        return "{}.{}".format(
            self._overwrite_namespace or self._origin_aspect_cls.NAMESPACE,
            self._func.__name__,
        )

    def __call__(self, *args, **kwargs):
        if self._func is None:
            self._func = args[0]
            return self

        if self._dispatcher is None:
            return self._call_internal(*args, **kwargs)

        return self._dispatcher.send(self.name, *args, **kwargs)

    def _call_internal(self, *args, **kwargs):
        logger.debug("Calling method {}".format(self._func))
        return self._func(self._aspect.__class__, *args, **kwargs)


class Delegate(DelegateBase):
    pass


class OverwriteDelegate(DelegateBase):
    pass


class MultiDelegate(DelegateBase):
    pass


class AddMultiDelegate(DelegateBase):
    pass


delegate = Delegate
overwrite_delegate = OverwriteDelegate
multi_delegate = MultiDelegate
add_multi_delegate = AddMultiDelegate

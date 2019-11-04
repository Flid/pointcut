from typing import NamedTuple, Type, List, Callable





class DelegateBase:
    def __init__(self):
        self._func = None
        self._dispatcher = None
        self._aspect = None

    def _bootstrap_dispatcher(self, dispatcher):
        self._dispatcher = dispatcher

    def _bootstrap_aspect(self, aspect):
        self._aspect = aspect

    @property
    def name(self):
        assert self._aspect.NAMESPACE
        return "{}.{}".format(self._aspect.NAMESPACE, self._func.__name__)

    def __call__(self, *args, **kwargs):
        if self._func is None:
            self._func = args[0]
            return self

        if self._dispatcher is None:
            return self._call_internal(*args, **kwargs)

        return self._dispatcher.send(self.name, *args, **kwargs)

    def _call_internal(self, *args, **kwargs):
        print("Calling method {}".format(self._func))
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

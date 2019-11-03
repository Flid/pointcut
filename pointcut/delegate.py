

class Delegate:
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
            return self._func(self._aspect, *args, **kwargs)

        import pdb; pdb.set_trace()

        return self._dispatcher.send(self.name, *args, **kwargs)

    def _call_internal(self, *args, **kwargs):
        print("Calling method {}".format(self._func))
        return self._func(self._aspect, *args, **kwargs)


class OverwriteDelegate(Delegate):
    pass


delegate = Delegate
overwrite_delegate = OverwriteDelegate

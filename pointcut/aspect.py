from .delegate import Delegate, DelegateBase


class DelegateRegisteringMeta(type):
    def __new__(mcls, name, bases, attrs, **kwargs):
        cls = super().__new__(mcls, name, bases, attrs, **kwargs)

        _DELEGATE_ATTRS = {}

        for base in reversed(bases):
            if hasattr(base, '_DELEGATE_ATTRS'):
                _DELEGATE_ATTRS.update(base._DELEGATE_ATTRS)

        for key, value in attrs.items():
            if isinstance(value, DelegateBase):
                _DELEGATE_ATTRS[key] = cls


        cls._DELEGATE_ATTRS = _DELEGATE_ATTRS
        return cls


class Aspect(metaclass=DelegateRegisteringMeta):
    NAMESPACE = None

    def __init__(self):
        for key, aspect_cls in self._DELEGATE_ATTRS.items():
            delegate = getattr(self, key)
            delegate._bootstrap_aspect(self, aspect_cls)

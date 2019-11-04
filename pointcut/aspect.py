from .delegate import Delegate, DelegateBase


class DelegateRegisteringMeta(type):
    def __new__(mcls, name, bases, attrs, **kwargs):
        cls = super().__new__(mcls, name, bases, attrs, **kwargs)

        cls._DELEGATE_ATTRS = set()

        for key, value in attrs.items():
            if isinstance(value, DelegateBase):
                cls._DELEGATE_ATTRS.add(key)

        cls._ALL_DELEGATE_ATTRS = set(cls._DELEGATE_ATTRS)

        for base in bases:
            if hasattr(base, '_ALL_DELEGATE_ATTRS'):
                cls._ALL_DELEGATE_ATTRS |= base._ALL_DELEGATE_ATTRS

        return cls


class Aspect(metaclass=DelegateRegisteringMeta):
    NAMESPACE = None

    def __init__(self):
        for key in self._ALL_DELEGATE_ATTRS:
            delegate = getattr(self, key)
            delegate._bootstrap_aspect(self)

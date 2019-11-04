from typing import List, Type, NamedTuple, Callable

from pointcut.exceptions import PointcutConfigurationError
from .aspect import Aspect
from .delegate import Delegate, OverwriteDelegate, MultiDelegate, \
    AddMultiDelegate, DelegateBase
import logging


logger = logging.getLogger(__name__)


class Handler:
    def __init__(self, namespace: str, name: str, delegate_cls: Type['Delegate'], delegates: List[DelegateBase]):
        self.namespace = namespace
        self.name = name
        self.delegate_cls = delegate_cls
        self.delegates = delegates

    @property
    def full_name(self):
        return '{}.{}'.format(self.namespace, self.name)

    @classmethod
    def from_delegate(cls, delegate: Delegate) -> 'Handler':
        return cls(
            namespace=delegate._aspect.NAMESPACE,
            name=delegate._func.__name__,
            delegate_cls=delegate.__class__,
            delegates=[delegate],
        )

    def call_internal(self, *args, **kwargs):
        if self.delegate_cls == Delegate:
            return self.delegates[-1]._call_internal(*args, **kwargs)
        elif self.delegate_cls == MultiDelegate:
            return [
                delegate._call_internal(*args, **kwargs)
                for delegate in self.delegates
            ]
        else:
            raise ValueError('Unknown delegate_cls {} for join point {}'.format(self.delegate_cls, self.full_name))


class PointcutDispatcher:
    def __init__(self, aspect_classes: List[Type[Aspect]] = None):
        self._aspects = []
        self._aspect_classes = set()
        self._handlers = {}
        self._register_aspects(aspect_classes or [])

    def _register_aspects(self, aspect_classes):
        for aspect_cls in aspect_classes:
            for cls in reversed(aspect_cls.__mro__):
                if not issubclass(cls, Aspect) or cls in self._aspect_classes:
                    continue

                self._aspect_classes.add(cls)
                self._register_new_aspect(cls)

    def _register_new_aspect(self, aspect_cls):
        logger.info('Registering aspect %s', aspect_cls.__name__)
        aspect = aspect_cls()
        self._aspects.append(aspect)

        def _add_new_handler(delegate):
            if delegate.name in self._handlers:
                raise PointcutConfigurationError(
                    'Aspect {} tries to define a delegate {}, which already exists'.format(
                        aspect_cls.__name__, delegate.name,
                    )
                )
            handler = Handler.from_delegate(delegate)
            self._handlers[delegate.name] = handler
            return handler

        def _append_delegate(delegate):
            if delegate.name not in self._handlers:
                raise PointcutConfigurationError(
                    'Aspect {} tries to modify a delegate {}, which does not exist yet'.format(
                        aspect_cls.__name__, delegate.name,
                    )
                )

            handler = self._handlers[delegate.name]
            handler.delegates.append(delegate)
            return handler

        for key in aspect_cls._DELEGATE_ATTRS:
            delegate = getattr(aspect, key)
            delegate._bootstrap_dispatcher(self)

            logger.debug('Registering delegate %s', delegate.name)

            if isinstance(delegate, MultiDelegate):
                _add_new_handler(delegate)
            elif isinstance(delegate, Delegate):
                _add_new_handler(delegate)
            elif isinstance(delegate, AddMultiDelegate):
                _append_delegate(delegate)
            elif isinstance(delegate, OverwriteDelegate):
                _append_delegate(delegate)

    def send(self, name, *args, **kwargs):
        print("Dispatching {}".format(name))
        handler = self._handlers[name]
        return handler.call_internal(*args, **kwargs)

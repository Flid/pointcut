from typing import List, Type

from pointcut.exceptions import PointcutConfigurationError
from .aspect import Aspect
from .delegate import Delegate, OverwriteDelegate
import logging


logger = logging.getLogger(__name__)


class PointcutDispatcher:
    def __init__(self, aspect_classes: List[Type[Aspect]]):
        self._aspects = []
        self._aspect_classes = set()
        self._handlers = {}
        self._register_aspects(aspect_classes)

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

        for key in aspect_cls._DELEGATE_ATTRS:
            member = getattr(aspect, key)
            member._bootstrap_dispatcher(self)

            logger.debug('Registering delegate %s', member.name)

            if isinstance(member, OverwriteDelegate):
                pass
            else:
                if member.name in self._handlers:
                    raise PointcutConfigurationError(
                        'Aspect {} tries to define a delegate {}, which already exists'.format(
                            aspect_cls.__name__, member.name,
                        )
                    )

            self._handlers[member.name] = member

    def send(self, name, *args, **kwargs):
        print("Dispatching {}".format(name))
        handler = self._handlers[name]
        return handler._call_internal(*args, **kwargs)

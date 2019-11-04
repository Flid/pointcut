from pointcut import Aspect, delegate, PointcutDispatcher


class ContextData:
    pass


class ContextAspect(Aspect):
    NAMESPACE = 'context'

    @delegate()
    def init(cls):
        return ContextData()

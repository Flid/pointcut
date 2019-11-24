from pointcut import Aspect, delegate, overwrite_delegate


class PipelineManagerAspect(Aspect):
    NAMESPACE = 'pipeline_manager'

    @delegate()
    def build_pipeline(cls):
        return 'I am a pipeline!'

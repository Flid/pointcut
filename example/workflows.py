from example.pipeline_manager import PipelineManagerAspect
from example.runner import RunnerAspect
from pointcut import Aspect, delegate


class WorkflowAspect(PipelineManagerAspect, RunnerAspect):
    @delegate()
    def kedro_run(cls):
        runner_data = cls.init_runner()
        pipeline = cls.build_pipeline()
        return cls.run_pipeline(runner_data=runner_data, pipeline=pipeline)

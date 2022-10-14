from abc import ABC, abstractmethod

class AbstractProvider(ABC):

    @abstractmethod
    def get_pipeline_id(self, pipeline_id=None, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def run_pipeline(self, pipeline_name=None, pipeline_id=None, **kwargs):
        raise NotImplementedError

class PipelineNotFound(Exception):
    pass
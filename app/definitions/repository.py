from abc import ABC, abstractmethod

from app.definitions.spec import BuildSpec


class BuildSpecRepository(ABC):

    @abstractmethod
    def get_build_spec(self, spec_name: str) -> BuildSpec:
        pass

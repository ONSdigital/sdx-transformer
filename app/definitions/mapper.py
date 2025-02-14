from abc import ABC, abstractmethod

from app.definitions.data import SurveyMetadata
from app.definitions.formatter import FormatterBase
from app.definitions.spec import BuildSpec


class Selector[T, U](ABC):

    @abstractmethod
    def choose(self, discriminator: T) -> U:
        pass


class Mapper[T, U]:

    def __init__(self, mappings: dict[str, Selector[T, U]]):
        self._mappings = mappings

    def get(self, key: str, discriminator: T) -> U:
        return self._mappings.get(key).choose(discriminator)


class SpecMapping[S](Mapper[S, str], ABC):

    @abstractmethod
    def get_build_spec(self, s: S) -> BuildSpec:
        pass


class BuildSpecMappingBase(SpecMapping[SurveyMetadata], ABC):

    @abstractmethod
    def get_build_spec(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        pass


class PrepopMappingBase(SpecMapping[str], ABC):

    @abstractmethod
    def get_build_spec(self, survey_id: str) -> BuildSpec:
        pass


class FormatterMappingBase[F: FormatterBase](Mapper[bool, str], ABC):

    @abstractmethod
    def get_formatter(self, target: str, looped: bool = False) -> F.__class__:
        pass

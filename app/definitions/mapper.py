"""
Definitions of the base Mapping classes.

The mapping base classes are built from the generic Mapper class - a data structure
allowing for dynamic mappings based on the implementation of the Selector interface.
"""

from abc import ABC, abstractmethod

from app.definitions.input import SurveyMetadata
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


class SpecMappingBase[S](Mapper[S, str], ABC):

    @abstractmethod
    def get_build_spec(self, s: S) -> BuildSpec:
        pass


class BuildSpecMappingBase(SpecMappingBase[SurveyMetadata], ABC):

    @abstractmethod
    def get_build_spec(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        pass


class PrepopMappingBase(SpecMappingBase[str], ABC):

    @abstractmethod
    def get_build_spec(self, survey_id: str) -> BuildSpec:
        pass


class FormatterMappingBase[F: FormatterBase](Mapper[bool, F.__class__], ABC):

    @abstractmethod
    def get_formatter(self, target: str, looped: bool = False) -> F.__class__:
        pass

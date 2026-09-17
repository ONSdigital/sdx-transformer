from abc import ABC, abstractmethod

from app.definitions.input import Data, Value, SurveyMetadata
from app.definitions.spec import ParseTree, BuildSpec
from app.services.formatters.formatter import Formatter


class TransformerBase(ABC):
    """
    Base class for all Transformers.
    A Transformer is responsible for all interactions with the build spec and the data.
    """

    @abstractmethod
    def get_spec(self) -> BuildSpec:
        pass

    @abstractmethod
    def interpolate(self) -> ParseTree:
        pass

    @abstractmethod
    def run(self, tree: ParseTree, data: Data) -> dict[str, Value]:
        pass

    @abstractmethod
    def get_formatter(self, survey_metadata: SurveyMetadata) -> Formatter:
        pass

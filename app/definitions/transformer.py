from abc import ABC, abstractmethod

from app.definitions.data import Data, Value
from app.definitions.formatter import FormatterBase
from app.definitions.spec import ParseTree, BuildSpec


class TransformerBase[F: FormatterBase](ABC):

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
    def get_formatter(self) -> F:
        pass

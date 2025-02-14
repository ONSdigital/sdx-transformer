from abc import ABC, abstractmethod

from app.definitions.data import Value, Data
from app.definitions.spec import ParseTree


class ExecutorBase(ABC):

    @abstractmethod
    def populate(self, tree: ParseTree, data: Data) -> ParseTree:
        pass

    @abstractmethod
    def execute(self, tree: ParseTree) -> dict[str, Value]:
        pass

from abc import ABC, abstractmethod

from app.definitions.input import Value, Data
from app.definitions.spec import ParseTree, Template, Transforms


class ExecutorBase(ABC):
    """
    Base class for all Executors.
    An Executor runs the main transformation steps.
    """

    @abstractmethod
    def interpolate(self, template: Template, transforms: Transforms) -> ParseTree:
        pass

    @abstractmethod
    def populate(self, tree: ParseTree, data: Data) -> ParseTree:
        pass

    @abstractmethod
    def execute(self, tree: ParseTree) -> dict[str, Value]:
        pass

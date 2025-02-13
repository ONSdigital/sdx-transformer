from typing import Optional

from app.definitions.mapper import Selector, Mapper
from app.definitions.spec import BuildSpecError
from app.formatters.formatter import Formatter
from app.formatters.looping_formatter import LoopingFormatter


class FormatterSelector(Selector[str, Formatter.__class__]):

    def __init__(self,
                 formatter: Formatter.__class__,
                 looped_formatter: Optional[LoopingFormatter.__class__] = None):
        self._formatter = formatter
        self._looping_formatter = looped_formatter

    def choose(self, looped: bool = False) -> Formatter.__class__:
        if looped and self._looping_formatter:
            return self._looping_formatter
        else:
            return self._formatter


class FormatterMapping(Mapper[bool, Formatter.__class__]):

    def __init__(self, mappings: dict[str, FormatterSelector]):
        super().__init__(mappings)

    def get(self, target: str, looped: bool = False) -> Formatter.__class__:
        selector = self._mappings.get(target)
        if not selector:
            raise BuildSpecError(f"Could not find formatter for {target}")

        return selector.choose(looped)

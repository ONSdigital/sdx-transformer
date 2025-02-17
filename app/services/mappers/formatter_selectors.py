from typing import Optional

from app.definitions.mapper import Selector
from app.services.formatters.formatter import Formatter
from app.services.formatters.looping_formatter import LoopingFormatter


class FormatterSelector(Selector[bool, Formatter.__class__]):

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

from typing import Literal

from app.definitions.spec import BuildSpec, ParseTree
from app.formatters.formatter import Formatter

template_type = Literal["template", "looped"]


class SpecReader:

    def get(self) -> BuildSpec:
        pass

    def interpolate(self, template: template_type = "template") -> ParseTree:
        pass

    def get_formatter[F: Formatter](self, looped: bool = False) -> F:
        pass

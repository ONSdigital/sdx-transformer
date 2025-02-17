from app.definitions.formatter import FormatterBase
from app.definitions.mapper import FormatterMappingBase
from app.definitions.spec import BuildSpecError
from app.services.mappers.formatter_selectors import FormatterSelector


class FormatterMapping[F: FormatterBase](FormatterMappingBase[F]):

    def __init__(self, mappings: dict[str, FormatterSelector]):
        super().__init__(mappings)

    def get_formatter(self, target: str, looped: bool = False) -> F.__class__:
        formatter: F.__class__ = self.get(target, looped)
        if not formatter:
            raise BuildSpecError(f"Could not find formatter for {target}")

        return formatter

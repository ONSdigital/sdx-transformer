from copy import deepcopy
from typing import Self, ClassVar, Optional

from app.definitions import ParseTree, Transform, Value


def execute(parse_tree: ParseTree) -> dict[str, str]:
    result: dict[str, str] = {}
    for k, v in parse_tree.items():
        if v is None or isinstance(v, str):
            result[k] = v
        else:
            result[k] = Function.from_transform(v).apply()

    return result


class Function:

    _function_lookup: ClassVar[dict[str, Self.__class__]] = []

    def __init__(self, value: Value, args: dict[str, str]):
        if value is None or isinstance(value, str):
            self._value = value
        else:
            self._value = Function.from_transform(value)
        self._args = args

    @classmethod
    def from_transform(cls, transform: Transform) -> Self:
        name = transform["name"]
        args = deepcopy(transform["args"])
        value = args.pop("value")
        return cls._function_lookup.get(name, cls)(value, args)

    @classmethod
    def set_function_lookup(cls, lookup: dict[str, Self.__class__]):
        cls._function_lookup = lookup

    def _get_value(self) -> Optional[str]:
        if not isinstance(self._value, str):
            return self._value.apply()
        else:
            return self._value

    def perform(self, value: Optional[str], **kwargs) -> Optional[str]:
        return value

    def apply(self) -> Optional[str]:
        v = self._get_value()
        return self.perform(v, **self._args)

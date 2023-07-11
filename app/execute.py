from copy import deepcopy

from app.definitions import ParseTree, Transform


def execute(parse_tree: ParseTree) -> dict[str, str]:
    result: dict[str, str] = {}
    for k, v in parse_tree.items():
        if not isinstance(v, str):
            result[k] = transform_to_function(v).apply()

    return result


class Function:

    def __init__(self, value, args: dict[str, str]):
        if isinstance(value, str):
            self._value = value
        else:
            self._value = transform_to_function(value)
        self._args = args

    def perform(self, v: str, kwargs) -> str:
        pass

    def apply(self) -> str:
        if not isinstance(self._value, str):
            v = self._value.apply()
        else:
            v = self._value

        return self.perform(v, self._args)


class Round(Function):

    def perform(self, v: str, kwargs) -> str:
        return round_up(v, **kwargs)


def round_up(v: str, precision: str) -> str:
    return "1"


def transform_to_function(transform: Transform) -> Function:
    name = transform["name"]
    args = deepcopy(transform["args"])
    value = args.pop("value")
    if name == "ROUND":
        return Round(value, args=args)



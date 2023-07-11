from copy import deepcopy

from app.definitions import ParseTree, Transform, Value


def execute(parse_tree: ParseTree) -> dict[str, str]:
    pass


class Function:

    def __int__(self, transform: Transform):
        self._value: Value = transform["args"]["value"]
        args = deepcopy(transform["args"])
        args.pop("value")
        self._args = args

    def apply(self):
        if isinstance(self._value, Transform):
            value = "do something?"





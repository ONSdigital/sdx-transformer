from typing import Final

from sdx_gcp.app import get_logger

from app.config.functions import function_lookup
from app.definitions.spec import ParseTree, Transform, BuildSpecError
from app.definitions.data import Value, Field
from app.transform.tree_walker import TreeWalker

logger = get_logger()


DERIVED_PREFIX: Final[str] = "&"
CURRENT_VALUE: Final[str] = DERIVED_PREFIX + "value"


def execute(tree: ParseTree) -> dict[str, Value]:
    """
    Convert a ParseTree into a dict of values by
    performing each transform as a function.
    The functions are looked up by name and then executed
    in reverse order (from leaf to root in the tree), so that each invocation
    either provides a value for its parent, or is the resulting value to be returned.
    """

    class ExecuteTreeWalker(TreeWalker):

        def on_dict(self, name: str, field: dict[str, Field]) -> Field:
            if 'name' in field.keys() and 'args' in field.keys():
                return execute_transform(field, self)

            return super().on_dict(name, field)

    def on_leaf(_name: str, field: str, walker: ExecuteTreeWalker) -> Field:
        if field.startswith(DERIVED_PREFIX) and field != CURRENT_VALUE:
            return walker.read_from_current(field[1:])

        return field

    return ExecuteTreeWalker(tree=tree, on_str=on_leaf).walk_tree()


def execute_transform(transform: Transform, walker: TreeWalker) -> Value | list[Value]:
    name = transform["name"]
    f = function_lookup.get(name)
    if f is None:
        raise BuildSpecError(f"Transform name {name} is not a valid function!")

    args = transform["args"]
    expanded_args: dict[str, Value] = {}
    for arg_name, arg_val in args.items():
        expanded_args[arg_name] = walker.evaluate_field(arg_name, arg_val)

    derived_args: dict[str, Value] = {}
    value: Value = expanded_args["value"]
    for expanded_name, expanded_val in expanded_args.items():
        if expanded_val == CURRENT_VALUE:
            derived_args[expanded_name] = value
        elif expanded_name != "value":
            derived_args[expanded_name] = expanded_val

    return f(value, **derived_args)

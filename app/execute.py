from collections.abc import Callable

from app.definitions import ParseTree, Transform, Field, Value, Empty
from app.functions.string import contains, any_contains, any_date, exists, concat, any_exists, to_date
from app.functions.numerical import round_half_up, aggregate, mean, number_equals
from app.tree_walker import TreeWalker

_function_lookup: dict[str, Callable] = {
    "CONTAINS": contains,
    "ANY_CONTAINS": any_contains,
    "TO_DATE": to_date,
    "ANY_DATE": any_date,
    "EXISTS": exists,
    "ANY_EXISTS": any_exists,
    "CONCAT": concat,
    "ROUND": round_half_up,
    "AGGREGATE": aggregate,
    "MEAN": mean,
    "NUMBER_EQUALS": number_equals,
}


def execute(tree: ParseTree) -> dict[str, Value]:
    class ExecuteTreeWalker(TreeWalker):

        def on_dict(self, name: str, field: dict[str, Field], walker: TreeWalker) -> Field:
            if 'name' in field.keys():
                return execute_transform(field, self)

            return super().on_dict(name, field, self)

    return ExecuteTreeWalker(tree=tree).walk_tree()


def execute_transform(transform: Transform, walker: TreeWalker) -> Value:
    name = transform["name"]
    f = _function_lookup.get(name)
    if f is None:
        return Empty

    args = transform["args"]
    expanded_args: dict[str, Value] = {}
    for arg_name, arg_val in args.items():
        expanded_args[arg_name] = walker.evaluate_field(arg_name, arg_val)

    return f(**expanded_args)

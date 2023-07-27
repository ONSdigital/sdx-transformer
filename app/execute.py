from collections.abc import Callable

from app.definitions import ParseTree, Transform, Field, Value, Empty
from app.functions.string import contains, any_contains, any_date, exists, concat, any_exists, to_date, no_transform, \
    starts_with
from app.functions.numerical import round_half_up, aggregate, mean, number_equals, total, divide
from app.tree_walker import TreeWalker


_function_lookup: dict[str, Callable] = {
    "VALUE": no_transform,
    "STARTS_WITH": starts_with,
    "CONTAINS": contains,
    "ANY_CONTAINS": any_contains,
    "TO_DATE": to_date,
    "ANY_DATE": any_date,
    "EXISTS": exists,
    "ANY_EXISTS": any_exists,
    "CONCAT": concat,
    "ROUND": round_half_up,
    "TOTAL": total,
    "DIVIDE": divide,
    "AGGREGATE": aggregate,
    "MEAN": mean,
    "NUMBER_EQUALS": number_equals,
}


def execute(tree: ParseTree) -> dict[str, Value]:
    """
    Convert a ParseTree into a dict of values by
    performing each transform as a function.
    The functions are looked up by name and then executed
    in reverse order (from leaf to root in the tree), so that each invocation
    either provides a value for its parent, or is the resulting value to be returned.
    """
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

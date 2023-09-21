from collections.abc import Callable
from typing import Final

from sdx_gcp.app import get_logger

from app.definitions import ParseTree, Transform, Field, Value, BuildSpecError
from app.functions.compound import currency_thousands, period_start, period_end
from app.functions.general import no_transform, exists, any_exists, lookup
from app.functions.numerical import round_half_up, aggregate, mean, number_equals, total, divide
from app.functions.string import starts_with, contains, any_contains, concat
from app.functions.time import to_date, any_date, start_of_month, end_of_month, start_of_year, end_of_year
from app.tree_walker import TreeWalker

logger = get_logger()


DERIVED_PREFIX: Final[str] = "&"
CURRENT_VALUE: Final[str] = DERIVED_PREFIX + "value"


_function_lookup: dict[str, Callable] = {
    "VALUE": no_transform,
    "EXISTS": exists,
    "ANY_EXISTS": any_exists,
    "LOOKUP": lookup,
    "STARTS_WITH": starts_with,
    "CONTAINS": contains,
    "ANY_CONTAINS": any_contains,
    "CONCAT": concat,
    "TO_DATE": to_date,
    "ANY_DATE": any_date,
    "START_OF_MONTH": start_of_month,
    "END_OF_MONTH": end_of_month,
    "START_OF_YEAR": start_of_year,
    "END_OF_YEAR": end_of_year,
    "ROUND": round_half_up,
    "TOTAL": total,
    "DIVIDE": divide,
    "AGGREGATE": aggregate,
    "MEAN": mean,
    "NUMBER_EQUALS": number_equals,
    "CURRENCY_THOUSANDS": currency_thousands,
    "PERIOD_START": period_start,
    "PERIOD_END": period_end,
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

        def on_dict(self, name: str, field: dict[str, Field]) -> Field:
            if 'name' in field.keys():
                return execute_transform(field, self)

            return super().on_dict(name, field)

    def on_leaf(_name: str, field: str, walker: ExecuteTreeWalker) -> Field:
        if field.startswith(DERIVED_PREFIX) and field != CURRENT_VALUE:
            derived = walker.read_from_current(field[1:])
            if derived is None:
                logger.warning(f"Failed to find derived value {field}")
            return derived

        return field

    return ExecuteTreeWalker(tree=tree, on_str=on_leaf).walk_tree()


def execute_transform(transform: Transform, walker: TreeWalker) -> Value:
    name = transform["name"]
    f = _function_lookup.get(name)
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

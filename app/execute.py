from collections.abc import Callable

from app.definitions import ParseTree, Transform, Field, Value, Empty
from app.functions.string import contains, any_contains, any_date, exists, concat, any_exists, to_date
from app.functions.numerical import round_half_up, aggregate, mean, number_equals

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


def execute(parse_tree: ParseTree) -> dict[str, Value]:
    result: dict[str, Value] = {}
    for k, v in parse_tree.items():
        if v is None or isinstance(v, str):
            result[k] = v
        else:
            result[k] = execute_transform(v)

    return result


def execute_transform(transform: Transform) -> Value:
    name = transform["name"]
    f = _function_lookup.get(name)
    if f is None:
        print(name)
        return Empty

    args = transform["args"]
    expanded_args: dict[str, Value] = {}
    for arg_name, arg_val in args.items():
        expanded_args[arg_name] = expand_field(arg_val)

    return f(**expanded_args)


def expand_field(field: Field) -> Value:
    if isinstance(field, dict):
        if 'name' in field.keys():
            return execute_transform(field)
        else:
            return {k: expand_field(v) for k, v in field.items()}
    elif isinstance(field, list):
        return [expand_field(v) for v in field]
    else:
        return field


def set_lookups(new_lookups: dict[str, Callable]):
    _function_lookup.clear()
    for k, v in new_lookups.items():
        _function_lookup[k] = v

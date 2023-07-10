from app.definitions import Template, Transforms, Transform, ParseTree

FUNCTION_PREFIX = "$"


def interpolate_functions(template: Template, transforms: Transforms) -> ParseTree:
    result: dict[str, Transform | str] = {}
    for k, v in template.items():
        if v.startswith(FUNCTION_PREFIX):
            result[k] = transforms[v]
        else:
            result[k] = v
    return result


def add_implicit_values(parse_tree: ParseTree) -> ParseTree:
    pass

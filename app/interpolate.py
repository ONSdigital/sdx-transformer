from app.definitions import Template, Transforms, Transform

FUNCTION_PREFIX = "$"


def interpolate_functions(template: Template, transforms: Transforms) -> dict[str, Transform | str]:
    result: dict[str, Transform | str] = {}
    for k, v in template.items():
        if v.startswith(FUNCTION_PREFIX):
            result[k] = transforms[v]
        else:
            result[k] = v
    return result

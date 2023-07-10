from app.definitions import Template, Transforms, Transform, ParseTree

FUNCTION_PREFIX = "$"


def interpolate_functions(template: Template, transforms: Transforms) -> ParseTree:
    result: dict[str, Transform | str] = {}

    for k, v in template.items():
        if v.startswith(FUNCTION_PREFIX):
            current_transform: Transform = transforms[v]

            if current_transform["post"]:
                new_result = result.copy()
                new_result["value"] = current_transform
                current_transform: Transform = transforms[current_transform["post"]]

                if current_transform["post"]:
                    temp_value = current_transform
                    temp_value["args"]["value"] = new_result["value"]
                    result_value = temp_value
                    current_transform: Transform = transforms[current_transform["post"]]

                    if "post" in current_transform:
                        temp_value = current_transform
                        temp_value["args"]["value"] = new_result["value"]
                        result_value = temp_value

                    else:
                        current_transform["args"]["value"] = temp_value
                        temp_value = current_transform
                        temp_value["args"]["value"] = result_value
                        result_value = temp_value

                    result[k] = result_value



            print(result)
        else:
            result[k] = v
    return result


def add_implicit_values(parse_tree: ParseTree) -> ParseTree:
    pass

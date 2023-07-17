from app.definitions import Submission, BuildSpec, ParseTree, Value
from app.execute import execute
from app.interpolate import interpolate


def create_pck(submission: Submission, build_spec: BuildSpec) -> str:
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"], submission["data"])
    result_data: dict[str, Value] = execute(parse_tree)
    return format(result_data)

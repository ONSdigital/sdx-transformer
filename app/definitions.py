from typing import TypedDict, NotRequired


Data = dict[str, str]

Template = dict[str, str]

Field = dict | list | str | None


class Transform(TypedDict):
    name: str
    args: dict[str, Field]
    post: NotRequired[str]


Transforms = dict[str, Transform]

Expression = Transform | str | None

Value = str | None

ParseTree = dict[str, Field]

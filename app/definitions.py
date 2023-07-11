from typing import TypedDict, NotRequired


Data = dict[str, str]

Template = dict[str, str]

Field = dict | list | str | None


class Transform(TypedDict):
    name: str
    args: dict[str, str | dict]
    post: NotRequired[str]


Transforms = dict[str, Transform]

ParseTree = dict[str, Transform | str]

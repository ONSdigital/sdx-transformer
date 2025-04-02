"""
Definitions describing the structure of a 'build spec'.
"""

from typing import TypedDict, NotRequired

from app.definitions.input import Field


Template = dict[str, Field]

ParseTree = dict[str, Field]


class Transform(TypedDict):
    name: str
    args: dict[str, Field]
    post: NotRequired[str]


Transforms = dict[str, Transform]


class BuildSpec(TypedDict):
    title: str
    survey_id: str
    period_format: str
    pck_period_format: NotRequired[str]
    form_mapping: NotRequired[dict[str, str]]
    target: str
    item_list_path: NotRequired[str]
    default_template: NotRequired[bool]
    template: Template
    looped: NotRequired[Template]
    transforms: Transforms


class BuildSpecError(Exception):
    pass

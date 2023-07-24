from typing import TypedDict, NotRequired


Data = dict[str, str]

Field = dict | list | str | None

Template = dict[str, Field]


class Transform(TypedDict):
    name: str
    args: dict[str, Field]
    post: NotRequired[str]


Transforms = dict[str, Transform]

Empty = None

Value = str | Empty

ParseTree = dict[str, Field]


class BuildSpec(TypedDict):
    title: str
    survey_id: str
    target: str
    item_list_path: NotRequired[str]
    template: Template
    transforms: Transforms


class SurveyMetadata(TypedDict):
    survey_id: str
    period_id: str
    ru_ref: str
    form_type: str


class Submission(TypedDict):
    tx_id: str
    metadata: SurveyMetadata
    data: Data


SubmissionJson = dict[str, dict[str, str] | str]

Identifier = str

PrepopData = dict[Identifier, list[Data]]

PCK = str

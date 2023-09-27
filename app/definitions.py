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
    period_format: str
    pck_period_format: NotRequired[str]
    form_mapping: NotRequired[dict[str, str]]
    target: str
    item_list_path: NotRequired[str]
    template: Template
    transforms: Transforms


iso_8601_date = str  # YYYY-MM-DD


class SurveyMetadata(TypedDict):
    survey_id: str
    period_id: str
    ru_ref: str
    form_type: str
    period_start_date: iso_8601_date
    period_end_date: iso_8601_date


Identifier = str

PrepopData = dict[Identifier, list[Data]]


PCK = str


class BuildSpecError(Exception):
    pass


class Answer(TypedDict):
    answer_id: str
    value: Field
    list_item_id: NotRequired[str]


class Group(TypedDict):
    items: list[str]
    name: str


class AnswerCode(TypedDict):
    answer_id: str
    code: str
    answer_value: NotRequired[str]


class ListCollector(TypedDict):
    answer_codes: list[AnswerCode]
    answers: list[Answer]
    lists: list[Group]


# Our top level looping object
class LoopedData(TypedDict):
    looped_sections: dict[str, list[Data]]
    data_section: dict[str, Value]

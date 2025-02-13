from typing import TypedDict, NotRequired


Empty = None
Value = str | Empty
Field = dict | list | str | None
Data = dict[str, str]
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


class Answer(TypedDict):
    answer_id: str
    value: Field
    list_item_id: NotRequired[str]


class SupplementaryDataMapping(TypedDict):
    identifier: str
    list_item_id: str


class Group(TypedDict):
    items: list[str]
    name: str
    supplementary_data_mappings: NotRequired[list[SupplementaryDataMapping]]


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
    looped_sections: dict[str, dict[str, Data]]
    data_section: dict[str, Value]


PCK = str


class SPPResponse(TypedDict):
    questioncode: str
    response: str
    instance: int


class SPP(TypedDict):
    formtype: str
    reference: str
    period: str
    survey: str
    responses: list[SPPResponse]


class ImageResponse(TypedDict):
    questioncode: str
    response: str
    instance: int
    sd_identifier: NotRequired[str]

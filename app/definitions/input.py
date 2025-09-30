"""
Definitions to describe the structure of the input data.
"""

from typing import TypedDict, NotRequired, TypeAlias

Empty: TypeAlias = None
Value = str | Empty
Field = dict | list | str | Empty
Data = dict[str, str]
iso_8601_date = str  # YYYY-MM-DD


class SurveyMetadata(TypedDict):
    survey_id: str
    period_id: str
    ru_ref: str
    form_type: str
    period_start_date: iso_8601_date
    period_end_date: iso_8601_date
    data_version: str


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


# The top level looping object
class LoopedData(TypedDict):
    looped_sections: dict[str, dict[str, Data]]
    data_section: dict[str, Value]

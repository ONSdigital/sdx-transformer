"""
Definitions to describe the structure of the output data.
"""

from typing import TypedDict


PCK = str
JSON = str


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

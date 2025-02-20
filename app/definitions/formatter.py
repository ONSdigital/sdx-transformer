"""
Definition of the Formatter Base.
A formatter is a responsible for generating the final output structure
after the transformations have taken place.
"""

from abc import ABC, abstractmethod

from app.definitions.input import Value, SurveyMetadata
from app.definitions.output import PCK


class FormatterBase(ABC):

    @abstractmethod
    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        pass

from abc import ABC, abstractmethod

from app.definitions.data import Value, SurveyMetadata, PCK


class FormatterBase(ABC):

    @abstractmethod
    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        pass

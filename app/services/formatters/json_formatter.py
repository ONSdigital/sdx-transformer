import json

from app.definitions.input import SurveyMetadata, Empty
from app.services.formatters.formatter import Formatter


class JsonFormatter(Formatter[tuple[str, str]]):
    """
    Format into json.
    """
    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> tuple[str, str]:
        return qcode, value

    def generate_output(self, metadata: SurveyMetadata) -> str:
        responses: list[tuple[str, str]] = self.evaluate_values()
        return json.dumps({r[0]: r[1] for r in responses if r[1] is not Empty})

import json

from app.definitions import Value, SurveyMetadata, PCK
from app.formatters.formatter import Formatter


class JSONFormatter(Formatter):
    """
    Format into json.
    """
    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        super().__init__(period_format, pck_period_format, form_mapping)

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        return json.dumps(data)

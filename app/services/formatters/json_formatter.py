import json

from app.definitions.data import SurveyMetadata, PCK, Empty, Value
from app.services.formatters.formatter import Formatter


class JSONFormatter(Formatter):
    """
    Format into json.
    """
    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        super().__init__(period_format, pck_period_format, form_mapping)

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        return json.dumps({k: v for k, v in data.items() if v is not Empty})

from app import get_logger
from app.definitions.input import SurveyMetadata, Empty
from app.services.formatters.pck_formatter import PckFormatter

logger = get_logger()


class OpenRoadFormatter(PckFormatter):
    """
    Formatter for Open Road systems.
    """
    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> str:
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]
        return f"{ru_ref}:{survey_id}:{period}:{qcode}:{value if value is not Empty else ''}"

from app.definitions.input import SurveyMetadata, Empty
from app.services.formatters.pck_formatter import PckFormatter


class CoraFormatter(PckFormatter):
    """
    Formatter for CORA systems.
    """
    _page: str = "1"

    def on_none(self) -> str:
        return ""

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> str:
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]
        return f"{survey_id}:{ru_ref}:{CoraFormatter._page}:{period}:{instance}:{qcode}:{value if value is not Empty else ''}"


class MesFormatter(CoraFormatter):

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> str:
        if instance == "0":
            instance = "00000"
        super().convert_value(qcode, value, instance, metadata)

from app.definitions.input import SurveyMetadata, Empty
from app.services.formatters.pck_formatter import PckFormatter


class CoraFormatter(PckFormatter):
    """
    Formatter for CORA systems.
    """
    def __init__(self, metadata: SurveyMetadata, period_format: str, pck_period_format: str,
                 form_mappings: dict[str, str]):
        super().__init__(metadata, period_format, pck_period_format, form_mappings)
        self.page: str = "1"
        self.instance: str = "0"

    def on_none(self) -> str:
        return ""

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> str:
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]
        return f"{survey_id}:{ru_ref}:{self.page}:{period}:{self.instance}:{qcode}:{value if value is not Empty else ''}"


class MesFormatter(CoraFormatter):

    def __init__(self, metadata: SurveyMetadata, period_format: str, pck_period_format: str,
                 form_mappings: dict[str, str]):
        super().__init__(metadata, period_format, pck_period_format, form_mappings)
        self.page: str = "1"
        self.instance: str = "00000"

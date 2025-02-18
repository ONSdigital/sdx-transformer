from app.definitions.input import SurveyMetadata, Empty, Value
from app.services.formatters.formatter import Formatter


class CORAFormatter(Formatter):
    """
    Formatter for CORA systems.
    """
    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        super().__init__(period_format, pck_period_format, form_mapping)
        self.page: str = "1"
        self.instance: str = "0"

    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        """Return a list of lines in a PCK file."""
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]

        return [
            f"{survey_id}:{ru_ref}:{self.page}:{period}:{self.instance}:{qcode}:{value if value is not Empty else ''}"
            for qcode, value in sorted(data.items())
        ]


class MESFormatter(CORAFormatter):
    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        super().__init__(period_format, pck_period_format, form_mapping)
        self.page: str = "1"
        self.instance: str = "00000"

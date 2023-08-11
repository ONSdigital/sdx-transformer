from app.definitions import Value, SurveyMetadata, Empty
from app.formatters.formatter import Formatter


class CORAFormatter(Formatter):
    """
    Formatter for CORA systems.
    """

    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        """Return a list of lines in a PCK file."""
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]
        page_identifier = "1"
        instance = "0"

        return [
            f"{survey_id}:{ru_ref}:{page_identifier}:{period}:{instance}:{qcode}:{value if value is not Empty else ''}"
            for qcode, value in sorted(data.items())
        ]

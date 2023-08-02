from sdx_gcp.app import get_logger

from app.definitions import Value, SurveyMetadata, Empty
from app.formatters.formatter import Formatter

logger = get_logger()


class OpenRoadFormatter(Formatter):
    """
    Formatter for Open Road systems.
    """

    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        """Return a list of lines in a PCK file."""
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]

        return [
            f"{ru_ref}:{survey_id}:{period}:{qcode}:{value if value is not Empty else ''}"
            for qcode, value in sorted(data.items())
        ]

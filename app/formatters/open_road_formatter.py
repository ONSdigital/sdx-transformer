from sdx_gcp.app import get_logger

from app.definitions import Value, SurveyMetadata
from app.formatters.formatter import Formatter

logger = get_logger()


class OpenRoadFormatter(Formatter):
    """
    Formatter for Open Road systems.
    """

    def __init__(self, data: dict[str, Value], metadata: SurveyMetadata):
        super().__init__(data, metadata)
        self._survey_id = metadata["survey_id"]

    def _pck_lines(self) -> list[str]:
        """Return a list of lines in a PCK file."""
        return [
            f"{self._ru_ref}:{self._survey_id}:{self._period}:{qcode}:{value}"
            for qcode, value in sorted(self._data.items())
        ]

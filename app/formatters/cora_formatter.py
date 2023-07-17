from app.definitions import Value, SurveyMetadata
from app.formatters.formatter import Formatter


class CORAFormatter(Formatter):
    """
    Formatter for CORA systems.
    """
    def __init__(self, data: dict[str, Value], metadata: SurveyMetadata):
        super().__init__(data, metadata)
        self._page_identifier = "1"
        self._instance = "0"

    def _pck_lines(self) -> list[str]:
        """Return a list of lines in a PCK file."""
        return [
            f"{self._survey_id}:{self._ru_ref}:{self._page_identifier}:{self._period}:{self._instance}:{qcode}:{value}"
            for qcode, value in sorted(self._data.items())
        ]

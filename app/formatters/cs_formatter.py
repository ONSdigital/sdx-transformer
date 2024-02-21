from app.definitions import SurveyMetadata, Value, PCK
from app.formatters.formatter import Formatter


class CSFormatter(Formatter):
    """
    Formatter for common software systems.
    """

    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        """Return a list of lines in a PCK file."""
        return self._pck_header(metadata) + self._pck_content(data)

    def _pck_header(self, metadata: SurveyMetadata) -> list[str]:
        return [
            "FV" + " " * 10,
            self._pck_form_header(metadata),
        ]

    def _pck_form_header(self, metadata: SurveyMetadata) -> str:
        """Generate a form header for PCK data."""
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        ru_check: str = ru[-1] if ru and ru[-1].isalpha() else ""
        period: str = self.convert_period(metadata["period_id"])
        form_type: str = self.get_form_type(metadata["form_type"])

        return f"{form_type}:{ru_ref}{ru_check}:{period}"

    def _pck_content(self, data: dict[str, Value]) -> list[str]:
        return [
            self._pck_item(q, a) for q, a in sorted(
                {int(k): int(v) for k, v in data.items() if v is not None}.items()
            )
        ]

    def _pck_item(self, q: int, a: int) -> str:
        """Return a PCK line item."""
        if a < 0:
            # CS can't handle negative numbers!
            a = 99999999999
        return "{0:04} {1:011}".format(q, a)

from typing import TypedDict

from app.definitions.input import Value, SurveyMetadata
from app.services.formatters.cs_formatter import CSFormatter

class AsheFormatter(CSFormatter):

    def _pck_content(self, data: dict[str, Value]) -> list[str]:
        """Generate the contents of a pck file as a list of strings"""
        return [
            self._pck_item(q, a) for q, a in sorted(
                {int(k): v for k, v in data.items() if v is not None}.items()
            )
        ]

    def _pck_item(self, q: int, a: int | str) -> str:
        """Return a PCK line item."""
        if a.isdigit():
            if int(a) < 0:
                # CS can't handle negative numbers!
                a = 99999999999
        return "{0:04} {1:011}".format(q, a)

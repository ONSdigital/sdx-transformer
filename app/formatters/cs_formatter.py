from app.formatters.formatter import Formatter


class CSFormatter(Formatter):
    """
    Formatter for common software systems.
    """

    def _pck_lines(self) -> list[str]:
        """Return a list of lines in a PCK file."""
        return [
            "FV" + " " * 10,
            self._pck_form_header(),
        ] + [
            self._pck_item(q, a) for q, a in sorted(self._data.items()) if a is not None
        ]

    def _pck_form_header(self) -> str:
        """Generate a form header for PCK data."""
        return f"{self._form_type}:{self._ru_ref}{self._ru_check}:{self._period}"

    def _pck_item(self, q, a) -> str:
        """Return a PCK line item."""
        try:
            v = int(a)
            if v < 0:
                # CS can't handle negative numbers!
                v = 99999999999
            return "{0:04} {1:011}".format(int(q), v)
        except ValueError:
            return f"{q} ???????????"

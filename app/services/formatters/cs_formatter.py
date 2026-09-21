from app.services.formatters.formatter import _SurveyMetadata
from app.services.formatters.pck_formatter import PckFormatter


class CsFormatter(PckFormatter):
    """
    Formatter for common software systems.
    """

    def convert_value(self, qcode: str, value: str, instance: str, metadata: _SurveyMetadata) -> str:
        if qcode.isdigit():
            q = int(qcode)
            if value.isdigit():
                v = int(value)
                if v < 0:
                    # CS can't handle negative numbers!
                    v = 99999999999
                return "{0:04} {1:011}".format(q, v)
            else:
                return "{0:04} {1}".format(q, value)
        else:
            return f"{qcode} {value}"

    def generate_header(self, metadata: _SurveyMetadata) -> list[str]:
        """Generate the header section for the pck as a list of strings"""
        return [
            "FV" + " " * 10,
            self._pck_form_header(metadata),
        ]

    def _pck_form_header(self, metadata: _SurveyMetadata) -> str:
        """Generate a form header for PCK data."""
        ru: str = metadata.ru_ref
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        ru_check: str = ru[-1] if ru and ru[-1].isalpha() else ""
        period: str = metadata.period_id
        form_type: str = metadata.form_type

        return f"{form_type}:{ru_ref}{ru_check}:{period}"

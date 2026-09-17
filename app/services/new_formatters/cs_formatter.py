from app.definitions.input import SurveyMetadata
from app.services.new_formatters.pck_formatter import PckFormatter


class CSFormatter(PckFormatter):
    """
    Formatter for common software systems.
    """

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> T:
        if value < 0:
            # CS can't handle negative numbers!
            value = 99999999999
        return "{0:04} {1:011}".format(int(qcode), int(value))

    def generate_header(self, metadata: SurveyMetadata) -> list[str]:
        """Generate the header section for the pck as a list of strings"""
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

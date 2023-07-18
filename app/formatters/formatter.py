from app.definitions import Value, SurveyMetadata


class Formatter:
    """
    Formatter for common software systems.
    """

    def __init__(self, data: dict[str, Value], metadata: SurveyMetadata):
        self._data = data
        ru: str = metadata["ru_ref"]
        self._ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        self._ru_check: str = ru[-1] if ru and ru[-1].isalpha() else ""
        self._period: str = metadata["period_id"]
        self._form_type: str = metadata["form_type"]
        self._survey_id = metadata["survey_id"]

    def get_pck(self) -> str:
        """Write a PCK file."""
        pck_lines = self._pck_lines()
        output = "\n".join(pck_lines)
        return output + "\n"

    def _pck_lines(self) -> list[str]:
        pass

    def pck_name(self, tx_id):
        """Generate the name of a PCK file."""
        return f"{self._survey_id}_{self._get_tx_code(tx_id)}"

    def _get_tx_code(self, tx_id: str) -> str:
        """Format the tx_id."""
        # tx_code is the first 16 digits of the tx_id without hyphens
        return "".join(tx_id.split("-"))[0:16]

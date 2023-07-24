from app.definitions import Value, SurveyMetadata, PCK


class Formatter:

    def __init__(self, data: dict[str, Value], metadata: SurveyMetadata):
        self._data = data
        ru: str = metadata["ru_ref"]
        self._ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        self._ru_check: str = ru[-1] if ru and ru[-1].isalpha() else ""
        self._period: str = metadata["period_id"]
        self._form_type: str = metadata["form_type"]
        self._survey_id = metadata["survey_id"]

    def generate_pck(self) -> PCK:
        """Write a PCK file."""
        pck_lines = self._pck_lines()
        output = "\n".join(pck_lines)
        return output + "\n"

    def _pck_lines(self) -> list[str]:
        pass

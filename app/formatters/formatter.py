from app.definitions import Value, SurveyMetadata, PCK, BuildSpecError
from app.period.period import PeriodFormatError, Period


class Formatter:

    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        self._period_format = period_format
        self._pck_period_format = pck_period_format
        self._form_mapping = form_mapping

    def get_form_type(self, form_type: str) -> str:
        if form_type in self._form_mapping:
            return self._form_mapping[form_type]
        else:
            return form_type

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        """Write a PCK file."""
        pck_lines = self._pck_lines(data, metadata)
        output = "\n".join(pck_lines)
        return output + "\n"

    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        pass

    def convert_period(self, period_id: str) -> str:
        try:
            period = Period(period_id, self._period_format)
            return period.convert_to_format(self._pck_period_format)

        except PeriodFormatError as e:
            raise BuildSpecError(f"Build spec period in wrong format {self._period_format}") from e

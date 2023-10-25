from app.definitions import Value, SurveyMetadata, PCK, BuildSpecError


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

    def convert_period(self, period: str) -> str:

        period_format = self._period_format

        # If the period does not match the period format,
        # use a default input format, based on the length of the period
        if len(period) != len(period_format):
            if len(period) == 6:
                period_format = "YYYYMM"
            elif len(period) == 4:
                period_format = "YYMM"
            elif len(period) == 2:
                period_format = "YY"

        symbols: dict[str, list[str]] = {
            "D": [],
            "M": [],
            "Y": []
        }

        for i in range(0, len(period)):
            k = period_format[i]
            if k not in symbols:
                raise BuildSpecError(f"Build spec period in wrong format {period_format}")
            symbols[k].append(period[i])

        if self._pck_period_format.count("Y") == 4:
            if len(symbols["Y"]) == 2:
                symbols["Y"].insert(0, "0")
                symbols["Y"].insert(0, "2")
        elif self._pck_period_format.count("Y") == 2:
            if len(symbols["Y"]) == 4:
                symbols["Y"].pop(0)
                symbols["Y"].pop(0)

        if self._pck_period_format.count("M") == 2:
            if len(symbols["M"]) == 0:
                symbols["M"].append("0")
                symbols["M"].append("1")

        result = ""
        for f in self._pck_period_format:
            result += symbols[f].pop(0)

        return result

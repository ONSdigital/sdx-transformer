from app.definitions import Value, SurveyMetadata, PCK, BuildSpecError


class Formatter:

    def __init__(self, period_format: str, pck_period_format: str):
        self._period_format = period_format
        self._pck_period_format = pck_period_format

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        """Write a PCK file."""
        pck_lines = self._pck_lines(data, metadata)
        output = "\n".join(pck_lines)
        return output + "\n"

    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        pass

    def convert_period(self, period: str) -> str:
        symbols: dict[str, list[str]] = {
            "D": [],
            "M": [],
            "Y": []
        }
        for i in range(0, len(period)):
            k = self._period_format[i]
            if k not in symbols:
                raise BuildSpecError(f"Build spec period in wrong format {self._period_format}")
            symbols[k].append(period[i])

        if self._pck_period_format.count("Y") == 4:
            if len(symbols["Y"]) == 2:
                symbols["Y"].insert(0, "0")
                symbols["Y"].insert(0, "2")
        elif self._pck_period_format.count("Y") == 2:
            if len(symbols["Y"]) == 4:
                symbols["Y"].pop(0)
                symbols["Y"].pop(0)

        result = ""
        for f in self._pck_period_format:
            result += symbols[f].pop(0)

        return result

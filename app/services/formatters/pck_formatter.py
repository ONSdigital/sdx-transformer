from abc import abstractmethod

from app.services.formatters.formatter import Formatter, _SurveyMetadata


class PckFormatter(Formatter[str]):

    @abstractmethod
    def convert_value(self, qcode: str, value: str, instance: str, metadata: _SurveyMetadata) -> str: ...

    def generate_output(self, metadata: _SurveyMetadata) -> str:
        header: list[str] = self.generate_header(metadata)
        pck_lines: list[str] = [line for line in self.evaluate_values() if line != ""]
        output = "\n".join(header + pck_lines)
        return output + "\n"

    def generate_header(self, metadata: _SurveyMetadata) -> list[str]:
        return []

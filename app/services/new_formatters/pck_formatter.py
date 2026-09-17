from app.definitions.input import SurveyMetadata
from app.services.new_formatters.formatter import Formatter


class PckFormatter(Formatter[str]):

    def generate_output(self, metadata: SurveyMetadata) -> str:
        header: list[str] = self.generate_header(metadata)
        pck_lines: list[str] = self.evaluate_values()
        output = "\n".join(header + pck_lines)
        return output + "\n"

    def generate_header(self, metadata: SurveyMetadata) -> list[str]:
        return []

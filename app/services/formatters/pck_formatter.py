from abc import abstractmethod

from app.services.formatters.formatter import Formatter, SubmissionMetadata


class PckFormatter(Formatter[str]):

    @abstractmethod
    def convert_value(self, qcode: str, value: str, instance: str, metadata: SubmissionMetadata) -> str: ...

    def generate_output(self, metadata: SubmissionMetadata) -> str:
        header: list[str] = self.generate_header(metadata)
        pck_lines: list[str] = [line for line in self.evaluate_values() if line != ""]
        output = "\n".join(header + pck_lines)
        return output + "\n"

    def generate_header(self, metadata: SubmissionMetadata) -> list[str]:
        return []

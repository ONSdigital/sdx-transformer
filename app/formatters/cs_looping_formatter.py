from app.definitions import Value, SurveyMetadata, PCK
from app.formatters.cs_formatter import CSFormatter
from app.formatters.looping_formatter import LoopingFormatter


class CSLoopingFormatter(CSFormatter, LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        pck_content: list[str] = self._pck_content(data_section)

        for instance_id, instance_data_list in self._instances.items():
            for instance_data in instance_data_list:
                data: dict[str, Value] = instance_data["data"]
                pck_content.extend(self._pck_content(data))

        pck_lines: list[str] = self._pck_header(metadata) + pck_content
        output = "\n".join(pck_lines)
        return output + "\n"

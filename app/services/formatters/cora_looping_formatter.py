from app.definitions.data import SurveyMetadata, PCK, Value
from app.services.formatters.cora_formatter import CORAFormatter
from app.services.formatters.looping_formatter import LoopingFormatter


class CORALoopingFormatter(CORAFormatter, LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        pck_lines: list[str] = self._pck_lines(data_section, metadata)

        for instance_id, instance_data_list in self._instances.items():
            for instance_data in instance_data_list:
                self.instance = instance_id
                data: dict[str, Value] = instance_data["data"]
                pck_lines.extend(self._pck_lines(data, metadata))

        output = "\n".join(pck_lines)
        return output + "\n"

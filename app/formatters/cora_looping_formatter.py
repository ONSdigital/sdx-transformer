from app.definitions import Value, SurveyMetadata, PCK
from app.formatters.cora_formatter import CORAFormatter
from app.formatters.looping_formatter import LoopingFormatter


class CORALoopingFormatter(CORAFormatter, LoopingFormatter):

	def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

		pck_lines: list[str] = self._pck_lines(data_section, metadata)

		for instance_id, data in self._instances.items():
			self.instance = instance_id
			pck_lines.extend(self._pck_lines(data, metadata))

		output = "\n".join(pck_lines)
		return output + "\n"

from app.definitions import Value, Data, SurveyMetadata, PCK
from app.formatters.cora_formatter import CORAFormatter


class CORALoopingFormatter(CORAFormatter):
	_instances: dict[str, Data] = {}

	def create_or_update_instance(self, instance_id: str, data: dict[str, Value]):

		# Update
		if instance_id in self._instances:
			self._instances[instance_id].update(data)

		# Create
		else:
			self._instances[instance_id] = data

	def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

		pck_lines: list[str] = self._pck_lines(data_section, metadata)

		for instance_id, data in self._instances.items():
			self.instance = instance_id
			pck_lines.extend(self._pck_lines(data, metadata))

		output = "\n".join(pck_lines)
		return output + "\n"



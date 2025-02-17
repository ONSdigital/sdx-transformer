import json

from app.definitions.data import SurveyMetadata, PCK, SPP, Value
from app.services.formatters.looping_formatter import LoopingFormatter
from app.services.formatters.spp_formatter import SPPFormatter


class SPPLoopingFormatter(SPPFormatter, LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        result: SPP = self.get_spp_template(data_section, metadata)

        for instance_id, instance_data_list in self._instances.items():
            for instance_data in instance_data_list:
                for qcode, value in instance_data["data"].items():
                    result['responses'].append({
                        "questioncode": qcode,
                        "response": value,
                        "instance": int(instance_id)
                    })

        return json.dumps(result)

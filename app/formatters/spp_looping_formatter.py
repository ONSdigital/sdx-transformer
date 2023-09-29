import json

from app.definitions import Value, SurveyMetadata, PCK, SPP
from app.formatters.looping_formatter import LoopingFormatter
from app.formatters.spp_formatter import SPPFormatter


class SPPLoopingFormatter(SPPFormatter, LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        result: SPP = self.get_spp_template(data_section, metadata)

        for instance_id, data in self._instances.items():
            for qcode, value in data.items():
                result['responses'].append({
                    "questioncode": qcode,
                    "response": value,
                    "instance": int(instance_id)
                })

        return json.dumps(result)

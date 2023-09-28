import json

from app.definitions import Value, SurveyMetadata, PCK, SPP
from app.formatters.looping_formatter import LoopingFormatter


class SPPFormatter(LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        result: SPP = {
            'formtype': metadata['form_type'],
            'reference': metadata['ru_ref'],
            'period': metadata['period_id'],
            'survey': metadata['survey_id'],
            'responses': []
        }

        for qcode, value in data_section.items():
            result['responses'].append({
                "questioncode": qcode,
                "response": value,
                "instance": 0
            })

        for instance_id, data in self._instances.items():
            for qcode, value in data.items():
                result['responses'].append({
                    "questioncode": qcode,
                    "response": value,
                    "instance": int(instance_id)
                })

        return json.dumps(result)

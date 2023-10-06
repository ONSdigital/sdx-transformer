import json

from app.definitions import Value, SurveyMetadata, PCK, SPP
from app.formatters.formatter import Formatter


class SPPFormatter(Formatter):

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        return json.dumps(self.get_spp_template(data, metadata))

    def get_spp_template(self, data: dict[str, Value], metadata: SurveyMetadata) -> SPP:
        result: SPP = {
            'formtype': metadata['form_type'],
            'reference': metadata['ru_ref'],
            'period': metadata['period_id'],
            'survey': metadata['survey_id'],
            'responses': []
        }

        for qcode, value in data.items():
            result['responses'].append({
                "questioncode": qcode,
                "response": value,
                "instance": 0
            })

        return result

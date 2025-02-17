import json

from app.definitions.data import SurveyMetadata, PCK, SPP, Empty, Value
from app.services.formatters.formatter import Formatter


class SPPFormatter(Formatter):

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        return json.dumps(self.get_spp_template(data, metadata))

    def get_spp_template(self, data: dict[str, Value], metadata: SurveyMetadata) -> SPP:
        ru_ref = metadata["ru_ref"]

        result: SPP = {
            'formtype': metadata['form_type'],
            'reference': ru_ref[0:-1] if ru_ref[-1].isalpha() else ru_ref,
            'period': metadata['period_id'],
            'survey': metadata['survey_id'],
            'responses': []
        }

        for qcode, value in data.items():
            if value is not Empty:
                result['responses'].append({
                    "questioncode": qcode,
                    "response": value,
                    "instance": 0
                })

        return result

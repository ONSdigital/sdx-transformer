import json

from app.definitions.input import SurveyMetadata
from app.definitions.output import SPPResponse, SPP
from app.services.new_formatters.formatter import Formatter


class SppFormatter(Formatter[SPPResponse]):

    def generate_output(self, metadata: SurveyMetadata) -> str:
        ru_ref = metadata["ru_ref"]

        result: SPP = {
            'formtype': metadata['form_type'],
            'reference': ru_ref[0:-1] if ru_ref[-1].isalpha() else ru_ref,
            'period': self.convert_period(metadata['period_id']),
            'survey': metadata['survey_id'],
            'responses': []
        }

        responses: list[SPPResponse] = self.evaluate_values()
        result["responses"] = responses
        return json.dumps(result)

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> SPPResponse:
        return {
            "questioncode": qcode,
            "response": value,
            "instance": int(instance)
        }

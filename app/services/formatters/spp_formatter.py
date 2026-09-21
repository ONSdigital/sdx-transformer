import json

from app.definitions.output import SPPResponse, SPP
from app.services.formatters.formatter import Formatter, SubmissionMetadata


class SppFormatter(Formatter[SPPResponse]):

    def generate_output(self, metadata: SubmissionMetadata) -> str:
        ru_ref = metadata.ru_ref

        result: SPP = {
            'formtype': metadata.form_type,
            'reference': ru_ref[0:-1] if ru_ref[-1].isalpha() else ru_ref,
            'period': metadata.period_id,
            'survey': metadata.survey_id,
            'responses': []
        }

        responses: list[SPPResponse] = self.evaluate_values()
        result["responses"] = responses
        return json.dumps(result)

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SubmissionMetadata) -> SPPResponse:
        return {
            "questioncode": qcode,
            "response": value,
            "instance": int(instance)
        }

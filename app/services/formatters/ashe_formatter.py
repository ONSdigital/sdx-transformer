from app.definitions.input import SurveyMetadata, Value
from app.services.formatters.pck_formatter import PckFormatter


class AsheFormatter(PckFormatter):

    def __init__(self, metadata: SurveyMetadata, period_format: str, pck_period_format: str,
                 form_mappings: dict[str, str]):
        super().__init__(metadata, period_format, pck_period_format, form_mappings)
        self._instance_ids: list[str] = []

    def read_instance(self, instance: str, data: dict[str, Value]) -> None:
        if instance not in self._instance_ids:
            self._instance_ids.append(instance)

    def _sub_header(self, instance: str, metadata: SurveyMetadata) -> str:
        """Generate a sub header for PCK data."""
        supplementary_data_mappings = self.get_supplementary_data_mappings()
        #nino = instance
        nino = self.get_nino_from_list_item_id(supplementary_data_mappings, instance)
        period = self.convert_period(metadata["period_id"])
        return f'FV\nHE{period}:{nino}:{period}'

    def get_nino_from_list_item_id(self, supplementary_data_mapping: list[dict[str, str]], list_item_id: str) -> Value:
        """Extract the nino from the supplementary data using the list_item_id"""
        for mapping in supplementary_data_mapping:
            for k, v in mapping.items():
                if v == list_item_id:
                    return mapping["identifier"]
        return None

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> str:
        line: str = self._get_value(qcode, value)
        if instance in self._instance_ids:
            # ensure header is written only once for each new instance
            self._instance_ids.remove(instance)
            header = self._sub_header(instance, metadata)
            return f'{header}\n{line}'
        else:
            return line

    def _get_value(self, qcode: str, value: str) -> str:
        if qcode.isdigit():
            q = int(qcode)
            if value.isdigit():
                v = int(value)
                if v < 0:
                    # CS can't handle negative numbers!
                    v = 99999999999
                return "{0:04} {1:011}".format(q, v)
            else:
                return "{0:04} {1}".format(q, value)
        else:
            return f"{qcode} {value}"

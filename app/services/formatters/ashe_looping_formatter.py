from app.definitions.input import Value, SurveyMetadata
from app.definitions.output import PCK
from app.services.formatters.ashe_formatter import AsheFormatter
from app.services.formatters.looping_formatter import LoopingFormatter


class AsheLoopingFormatter(AsheFormatter, LoopingFormatter):
    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        pck_content: list[str] = self._pck_content(data_section)

        for instance_id, instance_data_list in self._instances.items():
            for instance_data in instance_data_list:
                data: dict[str, Value] = instance_data["data"]

                supplementary_data = self.original_data["lists"][0]["supplementary_data_mappings"]
                nino: str = self.get_nino_from_list_item_id(supplementary_data, instance_data["list_item_id"])
                period: str = self.convert_period(metadata["period_id"])
                header: str = f'HE{period}:{nino}:{period}'

                pck_content.append("FV")
                pck_content.append(header)
                pck_content.extend(self._pck_content(data))

        # pck_lines: list[str] = self._pck_header(metadata) + pck_content
        output = "\n".join(pck_content)
        return output + "\n"

    def get_nino_from_list_item_id(self, supplementary_data_mapping: list[dict[str, str]], list_item_id: str) -> Value:
        """Extract the nino from the supplementary data using the list_item_id"""
        for mapping in supplementary_data_mapping:
            for k, v in mapping.items():
                if v == list_item_id:
                    return mapping["identifier"]
        return None

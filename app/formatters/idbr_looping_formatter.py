from app.definitions import Value, SurveyMetadata, PCK, SupplementaryDataMapping
from app.formatters.idbr_formatter import IDBRFormatter
from app.formatters.looping_formatter import LoopingFormatter


class IDBRLoopingFormatter(IDBRFormatter, LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        pck_lines: list[str] = self._pck_lines(data_section, metadata)

        sd_identifiers: dict[str, str] = {}
        for group in self.original_data["lists"]:
            if "supplementary_data_mappings" in group:
                mapping: SupplementaryDataMapping
                for mapping in group["supplementary_data_mappings"]:
                    sd_identifiers[mapping["list_item_id"]] = mapping["identifier"]

        for instance_id, instance_data_list in self._instances.items():
            for instance_data in instance_data_list:
                self.instance = instance_id
                data: dict[str, Value] = instance_data["data"]
                if instance_data["list_item_id"] in sd_identifiers:
                    identifier = sd_identifiers[instance_data["list_item_id"]]
                    pck_lines.extend(self._pck_lines(data, metadata, ref=identifier))
                else:
                    pck_lines.extend(self._pck_lines(data, metadata))

        output = "\n".join(pck_lines)
        return output + "\n"

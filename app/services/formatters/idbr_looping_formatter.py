from typing import Final

from app.definitions.input import SurveyMetadata, SupplementaryDataMapping, Value
from app.definitions.output import PCK
from app.services.formatters.idbr_formatter import IDBRFormatter
from app.services.formatters.looping_formatter import LoopingFormatter

DEFAULT_REF: Final[str] = "N0000000"
LIST_ITEM_ID: Final[str] = "list_item_id"


class IDBRLoopingFormatter(IDBRFormatter, LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        pck_lines: list[str] = self._pck_lines(data_section, metadata)
        sd_identifiers: dict[str, str] = {}
        site_mapping: dict[str, str] = {}

        for group in self.original_data["lists"]:
            if "supplementary_data_mappings" in group:
                mapping: SupplementaryDataMapping
                for mapping in group["supplementary_data_mappings"]:
                    sd_identifiers[mapping[LIST_ITEM_ID]] = mapping["identifier"]

            if group["name"] and group["name"] == "additional_sites_name":
                sites = group["items"]
                for i, site in enumerate(sites):
                    site_mapping[site] = f"N{str(i+1).zfill(len(DEFAULT_REF)-1)}"

        for instance_id, instance_data_list in self._instances.items():
            for instance_data in instance_data_list:
                data: dict[str, Value] = instance_data["data"]
                if instance_data[LIST_ITEM_ID] in sd_identifiers:
                    identifier = sd_identifiers[instance_data[LIST_ITEM_ID]]
                    pck_lines.extend(self._pck_lines(data, metadata, ref=identifier))
                else:
                    identifier = DEFAULT_REF
                    site: str = instance_data[LIST_ITEM_ID]
                    if site in site_mapping:
                        identifier = site_mapping[site]
                    pck_lines.extend(self._pck_lines(data, metadata, ref=identifier))

        output = "\n".join(pck_lines)
        return output + "\n"

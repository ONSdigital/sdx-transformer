import json

from app.definitions import Value, SurveyMetadata, PCK, ImageResponse, SupplementaryDataMapping
from app.formatters.looping_formatter import LoopingFormatter


class ImageLoopingFormatter(LoopingFormatter):

    def generate_pck(self, data_section: dict[str, Value], metadata: SurveyMetadata) -> PCK:

        sd_identifiers: dict[str, str] = {}
        for group in self.original_data["lists"]:
            if "supplementary_data_mappings" in group:
                mapping: SupplementaryDataMapping
                for mapping in group["supplementary_data_mappings"]:
                    sd_identifiers[mapping["list_item_id"]] = mapping["identifier"]

        result: list[ImageResponse] = []

        for qcode, value in data_section.items():
            result.append({
                "questioncode": qcode,
                "response": value,
                "instance": 0
            })

        for instance_id, instance_data_list in self._instances.items():
            for instance_data in instance_data_list:
                for qcode, value in instance_data["data"].items():
                    response: ImageResponse = {
                        "questioncode": qcode,
                        "response": value,
                        "instance": int(instance_id)
                    }

                    if instance_data["list_item_id"] in sd_identifiers:
                        identifier = sd_identifiers[instance_data["list_item_id"]]
                        response["sd_identifier"] = identifier

                    result.append(response)

        return json.dumps(result)

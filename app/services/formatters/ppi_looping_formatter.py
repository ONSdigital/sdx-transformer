from app.definitions.input import SurveyMetadata, Value
from app.definitions.output import PCK
from app.services.formatters.looping_formatter import LoopingFormatter


class PPILoopingFormatter(LoopingFormatter):
    """
    This class is used to format PPI data.
    It extends the LoopingFormatter class and overrides the generate_pck method.
    """

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        pck_lines: list[str] = []
        mappings = {mapping["list_item_id"]: mapping["identifier"] for mapping in
                    self.original_data["lists"][0]["supplementary_data_mappings"]}

        for instance_list in self._instances.values():
            for instance in instance_list:
                item_number = mappings.get(instance["list_item_id"], "")
                supplier_number = metadata["ru_ref"]
                period = metadata["period_id"]
                comment = "1" if instance["data"]["9996"] == "1" or data["9995"] == "1" else "0"
                price = instance["data"]["9997"]
                spec_marker = instance["data"]["9999"]

                pck_lines.append(
                    f"132:{supplier_number}:{period}:0:0:{comment}:0:{item_number}:{spec_marker}:0:{period}:01:0:{price}")

        output = "\n".join(pck_lines)
        return output + "\n"

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
        for instance_list in self._instances.values():
            for instance in instance_list:
                list_item_id = instance["list_item_id"]

                for mapping in self.original_data["lists"][0]["supplementary_data_mappings"]:
                    if mapping["list_item_id"] == list_item_id:
                        item_number = mapping["identifier"]
                        break

                supplier_number = metadata["ru_ref"]
                period = metadata["period_id"]

                if instance["data"]["9996"] == "1":
                    comment = "1"
                elif data["9995"] == "1":
                    comment = "1"
                else:
                    comment = "0"

                price = instance["data"]["9997"]

                pck_line = f"132:{supplier_number}:{period}:0:0:{comment}:0:{item_number}:9999:0:{period}:01:0:{price}"
                pck_lines.append(pck_line)

        output = "\n".join(pck_lines)
        return output + "\n"

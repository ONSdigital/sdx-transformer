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

        has_comment = False
        if data["9995"] == "1":
            has_comment = True
        if not has_comment:
            for instance_list in self._instances.values():
                for instance in instance_list:
                    if instance["data"]["9996"] == "1":
                        has_comment = True
                        break

        # PPI
        if metadata["survey_id"] == "132":
            for instance_list in self._instances.values():
                for instance in instance_list:
                    item_number = mappings.get(instance["list_item_id"], "")
                    ru = metadata["ru_ref"]
                    supplier: str = ru[0:-1] if ru[-1].isalpha() else ru
                    period = metadata["period_id"]
                    comment = "1" if has_comment else "0"
                    price = instance["data"]["9997"]
                    spec_marker = instance["data"]["9999"]

                    pck_lines.append(
                        f"132:{supplier}:{period}:0:0:{comment}:0:{item_number}:{spec_marker}:0:{period}:01:0:{price}")

        # EPI
        if metadata["survey_id"] == "133":
            for instance_list in self._instances.values():
                for instance in instance_list:
                    item_number = mappings.get(instance["list_item_id"], "")
                    ru = metadata["ru_ref"]
                    supplier: str = ru[0:-1] if ru[-1].isalpha() else ru
                    period = metadata["period_id"]
                    supplier_comment = "1" if has_comment else "0"
                    price = instance["data"]["9997"]
                    spec_marker = instance["data"]["9999"]

                    pck_lines.append(
                        f"133:{supplier}:{period}:0:0:{supplier_comment}:0:{item_number}:{spec_marker}:0:{period}:01:0:{price}")

        # IPI
        if metadata["survey_id"] == "133":
            for instance_list in self._instances.values():
                for instance in instance_list:
                    item_number = mappings.get(instance["list_item_id"], "")
                    ru = metadata["ru_ref"]
                    supplier: str = ru[0:-1] if ru[-1].isalpha() else ru
                    period = metadata["period_id"]
                    supplier_comment = "1" if has_comment else "0"
                    price = instance["data"]["9997"]
                    spec_marker = instance["data"]["9999"]

                    pck_lines.append(
                        f"156:{supplier}:{period}:0:0:{supplier_comment}:0:{item_number}:{spec_marker}:0:{period}:01:0:{price}")
        # SPPI
        elif metadata["survey_id"] == "061":
            for instance_list in self._instances.values():
                for instance in instance_list:
                    item_number = mappings.get(instance["list_item_id"], "")
                    ru = metadata["ru_ref"]
                    supplier: str = ru[0:-1] if ru[-1].isalpha() else ru
                    period = metadata["period_id"]
                    supplier_comment = "1" if has_comment else "0"
                    price = instance["data"]["9997"]
                    spec_marker = instance["data"]["9999"]

                    # Whitespace padding for PCK formatting
                    pck_lines.append(
                        f"061:{supplier}:{period}:0:0:{supplier_comment}:0:"
                        f"{item_number}:{spec_marker}:0:{period}:      :{price}"
                    )

        output = "\n".join(pck_lines)
        return output + "\n"

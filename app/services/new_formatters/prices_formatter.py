from dataclasses import dataclass

from app.definitions.input import SurveyMetadata, Value
from app.services.new_formatters.pck_formatter import PckFormatter


@dataclass
class _PricesInfo:
    price: str
    spec_marker: str
    comment_marker: str


class PricesFormatter(PckFormatter):
    """
    This class is used to format PPI data.
    It extends the LoopingFormatter class and overrides the generate_pck method.
    """

    def __init__(self, metadata: SurveyMetadata, period_format: str, pck_period_format: str,
                 form_mappings: dict[str, str]):
        super().__init__(metadata, period_format, pck_period_format, form_mappings)
        self._prices_info_mapping: dict[str, _PricesInfo] = {}   #instance:PricesLine
        self._has_comment = False

    def read_instance(self, instance: str, data: dict[str, Value]) -> None:
        if instance == "0":
            if "9995" in data:
                if data["9995"] == "1":
                    self._has_comment = True

            return

        comment_marker = "0"
        if self._has_comment:
            comment_marker = "1"
        else:
            if "9996" in data:
                if data["9996"] == "1":
                    comment_marker = "1"

        price = data["9997"]
        spec_marker = data["9999"]

        self._prices_info_mapping[instance] = _PricesInfo(
            price=price,
            spec_marker=spec_marker,
            comment_marker=comment_marker)

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> str:
        if instance in self._prices_info_mapping:
            prices_info = self._prices_info_mapping[instance]
            del self._prices_info_mapping[instance]
        else:
            return ""

        survey_id = metadata["survey_id"]
        item_number = instance
        ru = metadata["ru_ref"]
        supplier: str = ru[0:-1] if ru[-1].isalpha() else ru
        period = metadata["period_id"]
        comment = prices_info.comment_marker
        price = prices_info.price
        spec_marker = prices_info.spec_marker

        if survey_id == "061":
            return f"061:{supplier}:{period}:0:0:{comment}:0:{item_number}:{spec_marker}:0:{period}:      :{price}"

        else:
            return f"{survey_id}:{supplier}:{period}:0:0:{comment}:0:{item_number}:{spec_marker}:0:{period}:01:0:{price}"

        return ""

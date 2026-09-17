from app.definitions.spec import BuildSpecError
from app.services.formatters.spp_formatter import SPPFormatter
from app.services.new_formatters.ashe_formatter import AsheFormatter
from app.services.new_formatters.cora_formatter import CORAFormatter, MESFormatter
from app.services.new_formatters.cs_formatter import CSFormatter
from app.services.new_formatters.formatter import Formatter
from app.services.new_formatters.idbr_formatter import IDBRFormatter
from app.services.new_formatters.json_formatter import JSONFormatter
from app.services.new_formatters.open_road_formatter import OpenRoadFormatter
from app.services.new_formatters.prices_formatter import PricesFormatter


class FormatterMapping:

    def __init__(self):
        self._formatter_mapping = {
            "CORA": CORAFormatter,
            "CORA_MES": MESFormatter,
            "CS": CSFormatter,
            "OpenROAD": OpenRoadFormatter,
            "SPP": SPPFormatter,
            "IDBR": IDBRFormatter,
            "JSON": JSONFormatter,
            "PRICES": PricesFormatter,
            "ASHE": AsheFormatter,
        }

    def get_formatter(self, target: str) -> Formatter:
        formatter = self._formatter_mapping.get(target, None)
        if not formatter:
            raise BuildSpecError(f"Could not find formatter for {target}")

        return formatter

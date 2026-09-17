from app.definitions.spec import BuildSpecError
from app.services.formatters.spp_formatter import SppFormatter
from app.services.formatters.ashe_formatter import AsheFormatter
from app.services.formatters.cora_formatter import CoraFormatter, MesFormatter
from app.services.formatters.cs_formatter import CsFormatter
from app.services.formatters.formatter import Formatter
from app.services.formatters.idbr_formatter import IdbrFormatter
from app.services.formatters.json_formatter import JsonFormatter
from app.services.formatters.open_road_formatter import OpenRoadFormatter
from app.services.formatters.prices_formatter import PricesFormatter


class FormatterMapping:

    def __init__(self):
        self._formatter_mapping = {
            "CORA": CoraFormatter,
            "CORA_MES": MesFormatter,
            "CS": CsFormatter,
            "OpenROAD": OpenRoadFormatter,
            "SPP": SppFormatter,
            "IDBR": IdbrFormatter,
            "JSON": JsonFormatter,
            "PRICES": PricesFormatter,
            "ASHE": AsheFormatter,
        }

    def get_formatter(self, target: str) -> type[Formatter]:
        formatter = self._formatter_mapping.get(target, None)
        if not formatter:
            raise BuildSpecError(f"Could not find formatter for {target}")

        return formatter

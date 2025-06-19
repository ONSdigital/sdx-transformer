from app.services.formatters.ppi_looping_formatter import PPILoopingFormatter
from app.services.formatters.sppi_looping_formatter import SPPILoopingFormatter
from app.services.mappers.formatter_selectors import FormatterSelector
from app.services.formatters.cora_formatter import CORAFormatter, MESFormatter
from app.services.formatters.cora_looping_formatter import CORALoopingFormatter
from app.services.formatters.cs_formatter import CSFormatter
from app.services.formatters.cs_looping_formatter import CSLoopingFormatter
from app.services.formatters.idbr_looping_formatter import IDBRLoopingFormatter
from app.services.formatters.json_formatter import JSONFormatter
from app.services.formatters.open_road_formatter import OpenRoadFormatter
from app.services.formatters.spp_formatter import SPPFormatter
from app.services.formatters.spp_looping_formatter import SPPLoopingFormatter


_formatter_mapping = {
    "CORA": FormatterSelector(CORAFormatter, CORALoopingFormatter),
    "CORA_MES": FormatterSelector(MESFormatter),
    "CS": FormatterSelector(CSFormatter, CSLoopingFormatter),
    "OpenROAD": FormatterSelector(OpenRoadFormatter),
    "SPP": FormatterSelector(SPPFormatter, SPPLoopingFormatter),
    "IDBR": FormatterSelector(IDBRLoopingFormatter),
    "JSON": FormatterSelector(JSONFormatter),
    "PRICES": FormatterSelector(PPILoopingFormatter),
    "SPPI": FormatterSelector(SPPILoopingFormatter),
}

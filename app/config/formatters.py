from app.build_specs.formatter_selectors import FormatterSelector, FormatterMapping
from app.formatters.cora_formatter import CORAFormatter, MESFormatter
from app.formatters.cora_looping_formatter import CORALoopingFormatter
from app.formatters.cs_formatter import CSFormatter
from app.formatters.cs_looping_formatter import CSLoopingFormatter
from app.formatters.idbr_looping_formatter import IDBRLoopingFormatter
from app.formatters.json_formatter import JSONFormatter
from app.formatters.open_road_formatter import OpenRoadFormatter
from app.formatters.spp_formatter import SPPFormatter
from app.formatters.spp_looping_formatter import SPPLoopingFormatter


formatter_mapping: FormatterMapping = FormatterMapping({
    "CORA": FormatterSelector(CORAFormatter, CORALoopingFormatter),
    "CORA_MES": FormatterSelector(MESFormatter),
    "CS": FormatterSelector(CSFormatter, CSLoopingFormatter),
    "OpenROAD": FormatterSelector(OpenRoadFormatter),
    "SPP": FormatterSelector(SPPFormatter, SPPLoopingFormatter),
    "IDBR": FormatterSelector(IDBRLoopingFormatter),
    "JSON": FormatterSelector(JSONFormatter),
})

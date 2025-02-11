
from sdx_gcp.app import get_logger

from app.build_spec import get_build_spec, get_formatter, interpolate_build_spec
from app.definitions import BuildSpec, ParseTree, Value, PCK, Data, SurveyMetadata
from app.formatters.cora_formatter import CORAFormatter, MESFormatter
from app.formatters.cs_formatter import CSFormatter
from app.formatters.formatter import Formatter
from app.formatters.json_formatter import JSONFormatter
from app.formatters.open_road_formatter import OpenRoadFormatter
from app.formatters.spp_formatter import SPPFormatter
from app.build_specs.mappers import BuildSpecMapper, PeriodMapper
from app.build_specs.survey_mapping import SurveyMapping
from app.transform.execute import execute
from app.transform.populate import populate_mappings

logger = get_logger()

survey_mapping: SurveyMapping = SurveyMapping({
    "002": BuildSpecMapper("berd"),
    "009": PeriodMapper(period_id="2503", before="mbs", after_or_equal="mbs-spp"),
    "017": BuildSpecMapper("stocks"),
    "019": BuildSpecMapper("qcas"),
    "024": BuildSpecMapper("fuels"),
    "073": BuildSpecMapper("blocks"),
    "074": BuildSpecMapper("bricks"),
    "092": BuildSpecMapper("mes"),
    "127": BuildSpecMapper("mcg"),
    "134": BuildSpecMapper("mwss"),
    "139": BuildSpecMapper("qbs"),
    "144": BuildSpecMapper("ukis"),
    "160": BuildSpecMapper("qpses"),
    "165": BuildSpecMapper("qpsespb"),
    "169": BuildSpecMapper("qpsesrap"),
    "171": BuildSpecMapper("acas"),
    "182": BuildSpecMapper("vacancies"),
    "183": BuildSpecMapper("vacancies"),
    "184": BuildSpecMapper("vacancies"),
    "185": BuildSpecMapper("vacancies"),
    "187": BuildSpecMapper("des"),
    "194": BuildSpecMapper("rails"),
    "202": BuildSpecMapper("abs"),
    "228": BuildSpecMapper("construction"),
})


formatter_mapping: dict[str, Formatter.__class__] = {
    "CORA": CORAFormatter,
    "CORA_MES": MESFormatter,
    "CS": CSFormatter,
    "OpenROAD": OpenRoadFormatter,
    "SPP": SPPFormatter,
    "JSON": JSONFormatter,
}


def get_pck(submission_data: Data, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission data.
    """
    survey_name = survey_mapping.get_mapping(survey_metadata)
    build_spec: BuildSpec = get_build_spec(survey_name)
    add_metadata_to_input_data(submission_data, survey_metadata)
    transformed_data: dict[str, Value] = transform(submission_data, build_spec)
    formatter = get_formatter(build_spec, formatter_mapping)
    pck = formatter.generate_pck(transformed_data, survey_metadata)
    logger.info("Generated pck file")
    return pck


def add_metadata_to_input_data(submission_data: Data, survey_metadata: SurveyMetadata):
    for k, v in survey_metadata.items():
        submission_data[k] = v


def transform(data: Data, build_spec: BuildSpec) -> dict[str, Value]:
    full_tree: ParseTree = interpolate_build_spec(build_spec)
    populated_tree: ParseTree = populate_mappings(full_tree, data)
    result_data: dict[str, Value] = execute(populated_tree)
    logger.info("Completed data transformation")
    return result_data


from sdx_gcp.app import get_logger

from app.build_spec import get_build_spec, get_formatter, interpolate_build_spec
from app.definitions import BuildSpec, ParseTree, Value, PCK, Data, SurveyMetadata
from app.formatters.cora_formatter import CORAFormatter, MESFormatter
from app.formatters.cs_formatter import CSFormatter
from app.formatters.formatter import Formatter
from app.formatters.json_formatter import JSONFormatter
from app.formatters.open_road_formatter import OpenRoadFormatter
from app.formatters.spp_formatter import SPPFormatter
from app.mappers.mappers import SingleMapper, PeriodMapper
from app.mappers.survey_mapping import SurveyMapping
from app.transform.execute import execute
from app.transform.populate import populate_mappings

logger = get_logger()

survey_mapping: SurveyMapping = SurveyMapping({
    "002": SingleMapper("berd"),
    "009": PeriodMapper(period_id="2503", before="mbs", after_or_equal="mbs-spp"),
    "017": SingleMapper("stocks"),
    "019": SingleMapper("qcas"),
    "024": SingleMapper("fuels"),
    "073": SingleMapper("blocks"),
    "074": SingleMapper("bricks"),
    "092": SingleMapper("mes"),
    "127": SingleMapper("mcg"),
    "134": SingleMapper("mwss"),
    "139": SingleMapper("qbs"),
    "144": SingleMapper("ukis"),
    "160": SingleMapper("qpses"),
    "165": SingleMapper("qpsespb"),
    "169": SingleMapper("qpsesrap"),
    "171": SingleMapper("acas"),
    "182": SingleMapper("vacancies"),
    "183": SingleMapper("vacancies"),
    "184": SingleMapper("vacancies"),
    "185": SingleMapper("vacancies"),
    "187": SingleMapper("des"),
    "194": SingleMapper("rails"),
    "202": SingleMapper("abs"),
    "228": SingleMapper("construction"),
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

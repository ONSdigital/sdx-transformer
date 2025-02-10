import json
from collections.abc import Mapping
from os.path import exists
from typing import TypeVar, Literal

import yaml
from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, BuildSpecError, ParseTree, SurveyMetadata
from app.formatters.formatter import Formatter
from app.mappers.survey_mapping import SurveyMapping
from app.transform.interpolate import interpolate
from app.transform.populate import resolve_value_fields

logger = get_logger()


def get_build_spec(survey_name: str, subdir: str = "pck") -> BuildSpec:
    """
    Looks up the relevant build spec for the submission provided.
    """
    filepath = f"build_specs/{subdir}/{survey_name}.yaml"
    if exists(filepath):
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as y:
            build_spec: BuildSpec = yaml.safe_load(y.read())

    else:
        filepath = f"build_specs/{subdir}/{survey_name}.json"
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as j:
            build_spec: BuildSpec = json.load(j)

    return build_spec


template_type = Literal["template", "looped"]


def interpolate_build_spec(build_spec: BuildSpec, template: template_type = "template") -> ParseTree:
    if template == "looped":
        if template not in build_spec:
            template: template_type = "template"

    if 'transforms' in build_spec:
        parse_tree: ParseTree = interpolate(build_spec[template], build_spec["transforms"])
    else:
        parse_tree: ParseTree = build_spec[template]
    return resolve_value_fields(parse_tree)


T = TypeVar("T", bound=Formatter)


def get_formatter(build_spec: BuildSpec, formatter_mapping: Mapping[str, T.__class__]) -> T:
    f: T.__class__ = formatter_mapping.get(build_spec["target"])
    if f is None:
        raise BuildSpecError(f"Unable to find formatter for target: {build_spec['target']}")

    period_format = build_spec["period_format"]
    pck_period_format = build_spec["pck_period_format"] if "pck_period_format" in build_spec else period_format
    form_mapping = build_spec["form_mapping"] if "form_mapping" in build_spec else {}

    formatter: T = f(build_spec["period_format"], pck_period_format, form_mapping)
    return formatter

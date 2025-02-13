from typing import Literal

from app.build_specs.formatter_selectors import FormatterMapping
from app.build_specs.mappings import SpecMapping
from app.definitions import SurveyMetadata, BuildSpec, ParseTree, BuildSpecError
from app.formatters.formatter import Formatter
from app.transform.interpolate import interpolate
from app.transform.populate import resolve_value_fields


template_type = Literal["template", "looped"]


class BuildSpecReader[T]:

    def __init__(self, t: T, spec_mapping: SpecMapping[T], formatter_mapping: FormatterMapping):
        self._spec_mapping = spec_mapping
        self._formatter_mapping = formatter_mapping
        self._build_spec: BuildSpec = self._load(t)

    def _load(self, t: T) -> BuildSpec:
        pass

    def get(self) -> BuildSpec:
        return self._build_spec

    def interpolate(self, template: template_type = "template") -> ParseTree:
        build_spec = self._build_spec
        if template == "looped":
            if template not in build_spec:
                template: template_type = "template"

        if 'transforms' in build_spec:
            parse_tree: ParseTree = interpolate(build_spec[template], build_spec["transforms"])
        else:
            parse_tree: ParseTree = build_spec[template]
        return resolve_value_fields(parse_tree)

    def get_formatter[F: Formatter](self, looped: bool = False) -> F:
        build_spec = self._build_spec
        f: F.__class__ = self._formatter_mapping.get(build_spec["target"], looped)
        if f is None:
            raise BuildSpecError(f"Unable to find formatter for target: {build_spec['target']}")

        period_format = build_spec["period_format"]
        pck_period_format = build_spec["pck_period_format"] if "pck_period_format" in build_spec else period_format
        form_mapping = build_spec["form_mapping"] if "form_mapping" in build_spec else {}

        formatter: F = f(build_spec["period_format"], pck_period_format, form_mapping)
        return formatter


class PckSpecReader(BuildSpecReader[SurveyMetadata]):

    def _load(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        return self._spec_mapping.get_build_spec(survey_metadata["survey_id"], survey_metadata)


class PrepopSpecReader(BuildSpecReader[str]):

    def _load(self, survey_id: str) -> BuildSpec:
        return self._spec_mapping.get_build_spec(survey_id, "")

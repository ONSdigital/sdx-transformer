from abc import abstractmethod

from app.definitions.input import Data, Value, SurveyMetadata
from app.definitions.executor import ExecutorBase
from app.definitions.mapper import SpecMappingBase
from app.definitions.spec import BuildSpec, ParseTree, BuildSpecError
from app.definitions.transformer import TransformerBase
from app.services.formatters.formatter import Formatter, SubmissionMetadata
from app.services.mappers.formatter_mappings import FormatterMapping
from app.services.period.period import Period, PeriodFormatError
from app.services.transform.populate import resolve_value_fields


class SpecTransformer[S](TransformerBase):

    def __init__(self,
                 s: S,
                 spec_mapping: SpecMappingBase[S],
                 executor: ExecutorBase,
                 formatter_mapping: FormatterMapping):

        self._spec_mapping = spec_mapping
        self._executor = executor
        self._formatter_mapping = formatter_mapping
        self.looped = False
        self._build_spec: BuildSpec = self._load(s)

    @abstractmethod
    def _load(self, s: S) -> BuildSpec:
        pass

    def get_spec(self) -> BuildSpec:
        return self._build_spec

    def interpolate(self) -> ParseTree:
        build_spec = self._build_spec
        if 'transforms' in build_spec:
            parse_tree: ParseTree = self._executor.interpolate(build_spec["template"], build_spec["transforms"])
        else:
            parse_tree: ParseTree = build_spec["template"]
        return resolve_value_fields(parse_tree)

    def run(self, tree: ParseTree, data: Data) -> dict[str, Value]:
        populated_tree = self._executor.populate(tree, data)
        return self._executor.execute(populated_tree)

    def is_default(self) -> bool:
        return "default_template" in self._build_spec

    def get_formatter(self, survey_metadata: SurveyMetadata) -> Formatter:
        build_spec = self._build_spec
        metadata: SubmissionMetadata

        f: type[Formatter] = self._formatter_mapping.get_formatter(build_spec["target"])
        if f is None:
            raise BuildSpecError(f"Unable to find formatter for target: {build_spec['target']}")

        period_format = build_spec["period_format"]
        pck_period_format = build_spec["pck_period_format"] if "pck_period_format" in build_spec else period_format
        period = self._convert_period(survey_metadata["period_id"], period_format, pck_period_format)

        form_mapping = build_spec["form_mapping"] if "form_mapping" in build_spec else {}
        form_type = self._get_form_type(survey_metadata["form_type"], form_mapping)

        metadata = SubmissionMetadata(
            survey_id=survey_metadata["survey_id"],
            period_id=period,
            ru_ref=survey_metadata["ru_ref"],
            form_type=form_type,
        )

        formatter: Formatter = f(metadata)
        return formatter

    def _convert_period(self, period_id: str, period_format: str, pck_period_format: str) -> str:
        try:
            period = Period(period_id, period_format)
            return period.convert_to_format(pck_period_format)

        except PeriodFormatError as e:
            raise BuildSpecError(f"Build spec period in wrong format {period_format}") from e

    def _get_form_type(self, form_type: str, form_mappings: dict[str, str]) -> str:
        if form_type in form_mappings:
            return form_mappings[form_type]
        else:
            return form_type

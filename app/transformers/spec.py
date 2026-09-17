from abc import abstractmethod

from app.definitions.input import Data, Value, SurveyMetadata
from app.definitions.executor import ExecutorBase
from app.definitions.mapper import SpecMappingBase
from app.definitions.spec import BuildSpec, ParseTree, BuildSpecError
from app.definitions.transformer import TransformerBase
from app.services.formatters.formatter import Formatter
from app.services.mappers.formatter_mappings import FormatterMapping
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

    def get_formatter(self, survey_metadata: SurveyMetadata) -> Formatter:
        build_spec = self._build_spec
        f: type[Formatter] = self._formatter_mapping.get_formatter(build_spec["target"])
        if f is None:
            raise BuildSpecError(f"Unable to find formatter for target: {build_spec['target']}")

        period_format = build_spec["period_format"]
        pck_period_format = build_spec["pck_period_format"] if "pck_period_format" in build_spec else period_format
        form_mapping = build_spec["form_mapping"] if "form_mapping" in build_spec else {}

        formatter: Formatter = f(survey_metadata, build_spec["period_format"], pck_period_format, form_mapping)
        return formatter

from abc import ABC, abstractmethod

from app.definitions.data import Data, Value
from app.definitions.executor import ExecutorBase
from app.definitions.mapper import SpecMapping
from app.definitions.spec import BuildSpec, ParseTree, BuildSpecError
from app.definitions.transformer import TransformerBase
from app.mappers.formatter_mappings import FormatterMapping
from app.transform.interpolate import interpolate
from app.transform.populate import resolve_value_fields


class SpecTransformer[S, F](TransformerBase, ABC):

    def __init__(self,
                 s: S,
                 spec_mapping: SpecMapping[S],
                 executor: ExecutorBase,
                 formatter_mapping: FormatterMapping[F]):

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
            parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])
        else:
            parse_tree: ParseTree = build_spec["template"]
        return resolve_value_fields(parse_tree)

    def run(self, tree: ParseTree, data: Data) -> dict[str, Value]:
        populated_tree = self._executor.populate(tree, data)
        return self._executor.execute(populated_tree)

    def get_formatter(self,) -> F:
        build_spec = self._build_spec
        f: F.__class__ = self._formatter_mapping.get(build_spec["target"], self.looped)
        if f is None:
            raise BuildSpecError(f"Unable to find formatter for target: {build_spec['target']}")

        period_format = build_spec["period_format"]
        pck_period_format = build_spec["pck_period_format"] if "pck_period_format" in build_spec else period_format
        form_mapping = build_spec["form_mapping"] if "form_mapping" in build_spec else {}

        formatter: F = f(build_spec["period_format"], pck_period_format, form_mapping)
        return formatter

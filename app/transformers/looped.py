from typing import Literal

from app.definitions.data import SurveyMetadata
from app.definitions.spec import BuildSpec, ParseTree
from app.formatters.looping_formatter import LoopingFormatter
from app.transform.populate import resolve_value_fields
from app.transformers.standard import SpecTransformer

template_type = Literal["template", "looped"]


class LoopedPckSpecTransformer(SpecTransformer[SurveyMetadata, LoopingFormatter]):

    def _load(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        self.looped = True
        return self._spec_mapping.get_build_spec(survey_metadata)

    def interpolate_looped(self) -> ParseTree:
        build_spec = self._build_spec

        template: template_type = "looped"
        if "looped" not in build_spec:
            template = "template"

        if 'transforms' in build_spec:
            parse_tree: ParseTree = self._executor.interpolate(build_spec[template], build_spec["transforms"])
        else:
            parse_tree: ParseTree = build_spec[template]
        return resolve_value_fields(parse_tree)

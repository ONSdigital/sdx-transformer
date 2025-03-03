from typing import Literal

from app.definitions.input import SurveyMetadata
from app.definitions.spec import BuildSpec, ParseTree
from app.services.formatters.looping_formatter import LoopingFormatter
from app.services.transform.populate import resolve_value_fields
from app.transformers.spec import SpecTransformer

template_type = Literal["template", "looped"]


class LoopedSpecTransformer(SpecTransformer[SurveyMetadata, LoopingFormatter]):

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

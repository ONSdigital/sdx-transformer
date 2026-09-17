from app.definitions.input import SurveyMetadata
from app.definitions.spec import BuildSpec
from app.transformers.spec import SpecTransformer


class FlatSpecTransformer(SpecTransformer[SurveyMetadata]):

    def _load(self, s: SurveyMetadata) -> BuildSpec:
        return self._spec_mapping.get_build_spec(s)

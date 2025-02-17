from app.definitions.data import SurveyMetadata
from app.definitions.spec import BuildSpec
from app.formatters.formatter import Formatter
from app.transformers.standard import SpecTransformer


class FlatSpecTransformer(SpecTransformer[SurveyMetadata, Formatter]):

    def _load(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        return self._spec_mapping.get_build_spec(survey_metadata)

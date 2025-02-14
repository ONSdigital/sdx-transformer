from app.definitions.spec import BuildSpec
from app.transformers.standard import SpecTransformer


class PrepopTransformer(SpecTransformer[str, None]):

    def _load(self, survey_id: str) -> BuildSpec:
        return self._spec_mapping.get_build_spec(survey_id)
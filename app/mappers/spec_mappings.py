from app.definitions.mapper import BuildSpecMappingBase, Selector, PrepopMappingBase
from app.definitions.repository import BuildSpecRepository
from app.definitions.spec import BuildSpec
from app.definitions.data import SurveyMetadata


class BuildSpecMapping(BuildSpecMappingBase):

    def __init__(self, mappings: dict[str, Selector[SurveyMetadata, str]], repository: BuildSpecRepository):
        super().__init__(mappings)
        self._repository = repository

    def get_build_spec(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        spec_name: str = self.get(survey_metadata["survey_id"], survey_metadata)
        return self._repository.get_build_spec(spec_name)


class PrepopSpecMapping(PrepopMappingBase):

    def __init__(self, mappings: dict[str, Selector[str, str]], repository: BuildSpecRepository):
        super().__init__(mappings)
        self._repository = repository

    def get_build_spec(self, survey_id: str) -> BuildSpec:
        spec_name: str = self.get(survey_id, survey_id)
        return self._repository.get_build_spec(spec_name)

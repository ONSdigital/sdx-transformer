from sdx_gcp.errors import DataError

from app.definitions.mapper import Mapper, SpecMapping
from app.definitions.spec_repo import BuildSpecRepository
from app.definitions.spec import BuildSpec
from app.definitions.data import SurveyMetadata
from app.build_specs.spec_selectors import Selector


class BuildSpecMapping[T](SpecMapping[T]):

    def get_build_spec(self, survey_id: str, discriminator: T) -> BuildSpec:
        spec_name: str = self.get(survey_id, discriminator)
        return self._repository.get_build_spec(spec_name)


class PckSpecMapping(BuildSpecMapping[SurveyMetadata]):

    def __init__(self, mappings: dict[str, Selector[SurveyMetadata, str]], repository: BuildSpecRepository):
        super().__init__(mappings, repository)

    def get(self, survey_id: str, survey_metadata: SurveyMetadata) -> str:
        selector: Selector[SurveyMetadata, str] = self._mappings.get(survey_id)
        if not selector:
            raise DataError(f"Could not lookup survey id {survey_id}")

        return selector.choose(survey_metadata)


class PrepopBuildSpecMapping(BuildSpecMapping[str]):

    def __init__(self, mappings: dict[str, Selector[str, str]], repository: BuildSpecRepository):
        super().__init__(mappings, repository)

    def get(self, survey_id: str, _: str = "") -> str:
        selector = self._mappings.get(survey_id)
        if not selector:
            raise DataError(f"Could not lookup survey id {survey_id}")

        return selector.choose(_)

from sdx_gcp.errors import DataError

from app.build_specs.definitions import Mapper
from app.build_specs.reader import BuildSpecRepository
from app.definitions import SurveyMetadata, BuildSpec
from app.build_specs.spec_selectors import Selector


class SpecMapping[T](Mapper[T, str]):

    def __init__(self, mappings: dict[str, Selector[T, str]], repository: BuildSpecRepository):
        super().__init__(mappings)
        self._repository = repository

    def get_build_spec(self, survey_id: str, discriminator: T) -> BuildSpec:
        spec_name: str = self.get(survey_id, discriminator)
        return self._repository.get_build_spec(spec_name)


class BuildSpecMapping(SpecMapping[SurveyMetadata]):

    def __init__(self, mappings: dict[str, Selector[SurveyMetadata, str]], repository: BuildSpecRepository):
        super().__init__(mappings, repository)

    def get(self, survey_id: str, survey_metadata: SurveyMetadata) -> str:
        selector: Selector[SurveyMetadata, str] = self._mappings.get(survey_id)
        if not selector:
            raise DataError(f"Could not lookup survey id {survey_id}")

        return selector.choose(survey_metadata)


class PrepopBuildSpecMapping(SpecMapping[str]):

    def __init__(self, mappings: dict[str, Selector[str, str]], repository: BuildSpecRepository):
        super().__init__(mappings, repository)

    def get(self, survey_id: str, _: str = "") -> str:
        selector = self._mappings.get(survey_id)
        if not selector:
            raise DataError(f"Could not lookup survey id {survey_id}")

        return selector.choose(_)

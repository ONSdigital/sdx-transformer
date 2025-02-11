from sdx_gcp.errors import DataError

from app.definitions import SurveyMetadata
from app.build_specs.mappers import Mapper


class SurveyMapping:

    def __init__(self, mappings: dict[str, Mapper]):
        self._mappings = mappings

    def get_mapping(self, survey_metadata: SurveyMetadata) -> str:
        survey_id = survey_metadata["survey_id"]
        mapper = self._mappings.get(survey_id)
        if not mapper:
            raise DataError(f"Could not lookup survey id {survey_id}")

        return mapper.get_mapping(survey_metadata)

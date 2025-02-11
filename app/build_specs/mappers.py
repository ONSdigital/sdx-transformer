from app.build_specs.reader import read_build_spec
from app.definitions import SurveyMetadata, BuildSpec
from app.period.period import Period


class Mapper[T, U]:

    def get_mapping(self, discriminators: U) -> T:
        pass


class PckSpecMapper(Mapper[BuildSpec, SurveyMetadata]):

    def __init__(self, spec_name: str):
        self._spec_name = spec_name

    def get_mapping(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        return read_build_spec(self._spec_name, subdir="pck")


class PckPeriodMapper(Mapper):

    def __init__(self, period_id, before: str, after_or_equal: str):
        self._period_id = period_id
        self._before = before
        self._after_or_equal = after_or_equal

    def get_mapping(self, survey_metadata: SurveyMetadata) -> BuildSpec:
        period = Period(survey_metadata["period_id"])
        spec_name: str
        if period < Period(self._period_id):
            spec_name = self._before
        else:
            spec_name = self._after_or_equal

        return read_build_spec(spec_name, subdir="pck")

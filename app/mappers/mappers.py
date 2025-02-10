from app.definitions import SurveyMetadata


class Mapper:

    def get_mapping(self, survey_metadata: SurveyMetadata):
        pass


class SingleMapper(Mapper):

    def __init__(self, mapping: str):
        self._mapping = mapping

    def get_mapping(self, survey_metadata: SurveyMetadata):
        return self._mapping


class PeriodMapper(Mapper):

    def __init__(self, period_id, before: str, after_or_equal: str):
        self._period_id = period_id
        self._before = before
        self._after_or_equal = after_or_equal

    def get_mapping(self, survey_metadata: SurveyMetadata):
        period = survey_metadata["period_id"]
        if period < self._period_id:
            return self._before
        else:
            return self._after_or_equal

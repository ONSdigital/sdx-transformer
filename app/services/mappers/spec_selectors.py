from app.definitions.mapper import Selector
from app.definitions.input import SurveyMetadata
from app.services.period.period import Period


class PrepopSelector(Selector[str, str]):
    def __init__(self, spec_name: str):
        self._spec_name = spec_name

    def choose(self, discriminator: str = "") -> str:
        return self._spec_name


class BuildSpecSelector(Selector[SurveyMetadata, str]):

    def __init__(self, spec_name: str):
        self._spec_name = spec_name

    def choose(self, discriminator: SurveyMetadata) -> str:
        return self._spec_name


class BuildSpecPeriodSelector(BuildSpecSelector):

    def __init__(self, period_id, before: str, after_or_equal: str):
        super().__init__(before)
        self._period_id = period_id
        self._before = before
        self._after_or_equal = after_or_equal

    def choose(self, discriminator: SurveyMetadata) -> str:
        period = Period(discriminator["period_id"])
        spec_name: str
        if period < Period(self._period_id):
            spec_name = self._before
        else:
            spec_name = self._after_or_equal

        return spec_name

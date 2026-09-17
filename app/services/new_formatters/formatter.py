from abc import abstractmethod, ABC

from app.definitions.spec import BuildSpecError, BuildSpec
from app.definitions.input import SurveyMetadata, Value
from app.services.period.period import PeriodFormatError, Period


class Formatter[T](ABC):

    def __init__(self, spec: BuildSpec, metadata: SurveyMetadata):
        self._spec = spec
        self._metadata = metadata
        self._instances: dict[str, dict[str, Value]] = {}   # key=instance_id

    def create_or_update_instance(self, instance_id: str, data: dict[str, Value]):
        if instance_id not in self._instances:
            self._instances[instance_id] = {}

        self._instances[instance_id].update(data)

    # def get_metadata(self) -> SurveyMetadata:
    #     return self._metadata

    def get_form_type(self, form_type: str) -> str:
        if form_type in self._spec["form_mapping"]:
            return self._spec["form_mapping"][form_type]
        else:
            return form_type

    @abstractmethod
    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> T: ...

    def evaluate_values(self) -> list[T]:
        results: list[T] = []
        for instance, data in self._instances.items():
            for qcode, value in data.items():
                results.append(self.convert_value(qcode, value, instance))

        return results

    def create_output(self) -> str:
        return self.generate_output(self._metadata)

    @abstractmethod
    def generate_output(self, metadata: SurveyMetadata) -> str: ...

    def convert_period(self, period_id: str) -> str:
        try:
            period = Period(period_id, self._spec["period_format"])
            return period.convert_to_format(self._spec["pck_period_format"])

        except PeriodFormatError as e:
            raise BuildSpecError(f"Build spec period in wrong format {self._spec["period_format"]}") from e

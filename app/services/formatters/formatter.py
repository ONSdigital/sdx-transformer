from abc import abstractmethod, ABC
from typing import Optional

from app.definitions.spec import BuildSpecError
from app.definitions.input import SurveyMetadata, Value
from app.services.period.period import PeriodFormatError, Period


class Formatter[T](ABC):

    def __init__(self, metadata: SurveyMetadata, period_format: str, pck_period_format: str, form_mappings: dict[str, str]):
        self._metadata: SurveyMetadata = metadata
        self._period_format: str = period_format
        self._pck_period_format: str = pck_period_format
        self._form_mappings: dict[str, str] = form_mappings
        self._instances: dict[str, dict[str, Value]] = {}   # key=instance_id

    def create_or_update_instance(self, instance_id: str, data: dict[str, Value]) -> None:
        if instance_id not in self._instances:
            self._instances[instance_id] = {}

        self._instances[instance_id].update(data)

    def get_form_type(self, form_type: str) -> str:
        if form_type in self._form_mappings:
            return self._form_mappings[form_type]
        else:
            return form_type

    @abstractmethod
    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> T: ...

    def prepare_instance(self, instance: str, data: dict[str, Value]) -> dict[str, Value]:
        return data

    def on_none(self) -> Optional[T]:
        return None

    def evaluate_values(self) -> list[T]:
        results: list[T] = []
        for instance, data in self._instances.items():
            data = self.prepare_instance(instance, data)
            for qcode, value in data.items():
                if value is None:
                    print(f"none value for qcode: {qcode}, instance: {instance}")
                    value = self.on_none()

                if value is not None:
                    results.append(self.convert_value(qcode, value, instance, self._metadata))

        return results

    def create_output(self) -> str:
        return self.generate_output(self._metadata)

    @abstractmethod
    def generate_output(self, metadata: SurveyMetadata) -> str: ...

    def convert_period(self, period_id: str) -> str:
        try:
            period = Period(period_id, self._period_format)
            return period.convert_to_format(self._pck_period_format)

        except PeriodFormatError as e:
            raise BuildSpecError(f"Build spec period in wrong format {self._period_format}") from e

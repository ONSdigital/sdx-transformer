from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Optional

from app.definitions.input import Value


@dataclass
class SubmissionMetadata:
    survey_id: str
    period_id: str
    ru_ref: str
    form_type: str


class Formatter[T](ABC):

    def __init__(self, metadata: SubmissionMetadata):
        self._metadata: SubmissionMetadata = metadata
        self._instances: dict[str, dict[str, Value]] = {}   # key=instance_id

    def add_data(self, instance_id: str, data: dict[str, Value]) -> None:
        if instance_id not in self._instances:
            self._instances[instance_id] = {}

        self._instances[instance_id].update(data)

    @abstractmethod
    def convert_value(self, qcode: str, value: str, instance: str, metadata: SubmissionMetadata) -> T: ...

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
                    value = self.on_none()

                if value is not None:
                    results.append(self.convert_value(qcode, value, instance, self._metadata))

        return results

    def create_output(self) -> str:
        return self.generate_output(self._metadata)

    @abstractmethod
    def generate_output(self, metadata: SubmissionMetadata) -> str: ...

from typing import TypedDict

from app.definitions.input import ListCollector, Value
from app.services.formatters.formatter import Formatter


class InstanceData(TypedDict):
    data: dict[str, Value]
    list_item_id: str


class LoopingFormatter(Formatter):

    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        super().__init__(period_format, pck_period_format, form_mapping)
        self._instances: dict[str, list[InstanceData]] = {}
        self.supplementary_data_mappings = None

    def set_original(self, supplementary_data_mappings: dict[str, str]):
        self.supplementary_data_mappings = supplementary_data_mappings

    def create_or_update_instance(self, instance_id: str, data: dict[str, Value], list_item_id: str = ""):
        if instance_id not in self._instances:
            self._instances[instance_id] = []

        self._instances[instance_id].append({
            "data": data,
            "list_item_id": list_item_id
        })

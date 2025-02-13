from typing import TypedDict

from app.definitions.data import ListCollector, Value
from app.formatters.formatter import Formatter


class InstanceData(TypedDict):
    data: dict[str, Value]
    list_item_id: str


class LoopingFormatter(Formatter):

    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        super().__init__(period_format, pck_period_format, form_mapping)
        self._instances: dict[str, list[InstanceData]] = {}
        self.original_data = None

    def set_original(self, original_data: ListCollector):
        self.original_data = original_data

    def create_or_update_instance(self, instance_id: str, data: dict[str, Value], list_item_id: str = ""):
        if instance_id not in self._instances:
            self._instances[instance_id] = []

        self._instances[instance_id].append({
            "data": data,
            "list_item_id": list_item_id
        })

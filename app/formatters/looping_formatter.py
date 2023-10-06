from app.definitions import Data, Value, Empty
from app.formatters.formatter import Formatter


class LoopingFormatter(Formatter):

    def __init__(self, period_format: str, pck_period_format: str, form_mapping: dict[str, str] = {}):
        super().__init__(period_format, pck_period_format, form_mapping)
        self._instances: dict[str, Data] = {}

    def create_or_update_instance(self, instance_id: str, data: dict[str, Value]):

        # Update
        if instance_id in self._instances:
            self._instances[instance_id].update(data)

        # Create
        else:
            self._instances[instance_id] = data

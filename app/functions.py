from typing import Optional

from app.execute import Function


class Contains(Function):
    def perform(self,
                value: Optional[str],
                match_str: str = "",
                on_true: str = "1",
                on_false: str = "2") -> Optional[str]:

        if value is None:
            return None
        if match_str in value:
            return on_true
        return on_false


class Exists(Function):
    def perform(self, value: Optional[str], on_true: str = "1", on_false: str = "2") -> Optional[str]:
        if value is not None:
            return on_true
        return on_false

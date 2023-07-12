from typing import Optional, List
from datetime import datetime, date, timezone

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


class AnyContains(Function):
    def perform(self,
                value: Optional[str],
                values: List[Optional[str]] = [],
                match_str: str = "",
                on_true: str = "1",
                on_false: str = "2") -> Optional[str]:
        all_values = [value] + values
        for val in all_values:
            if val is not None:
                if match_str in val:
                    return on_true
        return on_false


class AnyDate(Function):
    def perform(self,
                value: Optional[str],
                values: List[Optional[str]] = [],
                on_true: str = "1",
                on_false: str = "2") -> Optional[str]:
        all_values = [value] + values
        for val in all_values:
            if val is not None:
                if _is_date(val):
                    return on_true
        return on_false


class Exists(Function):
    def perform(self, value: Optional[str], on_true: str = "1", on_false: str = "2") -> Optional[str]:
        if value is not None:
            return on_true
        return on_false


def _is_date(text: str) -> bool:
    try:
        datetime.strptime(text, "%d/%m/%Y").date()
        return True
    except ValueError:
        return False

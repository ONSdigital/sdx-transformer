from app.execute import Function


class Matches(Function):
    def perform(self,
                value: str,
                match_str: str = "",
                match_type: str = "contains",
                on_true: str = "1",
                on_false: str = "2") -> str:
        if match_str in value:
            return on_true
        return on_false


class Exists(Function):
    def perform(self, value: str, on_true: str = "1", on_false: str = "2") -> str:
        pass


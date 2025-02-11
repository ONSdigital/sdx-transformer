from collections.abc import Mapping
from typing import Literal

from app.definitions import BuildSpec, ParseTree, BuildSpecError
from app.formatters.formatter import Formatter
from app.transform.interpolate import interpolate
from app.transform.populate import resolve_value_fields

template_type = Literal["template", "looped"]


class BuildSpecImpl:

    def __init__(self, spec: BuildSpec):
        self._build_spec = spec

    def interpolate(self, template: template_type = "template") -> ParseTree:
        if template == "looped":
            if template not in self._build_spec:
                template: template_type = "template"

        if 'transforms' in self._build_spec:
            parse_tree: ParseTree = interpolate(self._build_spec[template], self._build_spec["transforms"])
        else:
            parse_tree: ParseTree = self._build_spec[template]
        return resolve_value_fields(parse_tree)

    def get_formatter[F: Formatter](self, formatter_mapping: Mapping[str, F.__class__]) -> F:
        f: F.__class__ = formatter_mapping.get(self._build_spec["target"])
        if f is None:
            raise BuildSpecError(f"Unable to find formatter for target: {self._build_spec['target']}")

        period_format = self._build_spec["period_format"]
        pck_period_format = self._build_spec["pck_period_format"] if "pck_period_format" in self._build_spec else period_format
        form_mapping = self._build_spec["form_mapping"] if "form_mapping" in self._build_spec else {}

        formatter: F = f(self._build_spec["period_format"], pck_period_format, form_mapping)
        return formatter

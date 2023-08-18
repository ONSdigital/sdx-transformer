from app.definitions import SurveyMetadata, Value, PCK
from app.formatters.formatter import Formatter


class CSFormatter(Formatter):
    """
    Formatter for common software systems.
    """

    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        """Return a list of lines in a PCK file."""
        return [
            "FV" + " " * 10,
            self._pck_form_header(metadata),
        ] + [
            self._pck_item(q, a) for q, a in sorted(
                {int(k): int(v) for k, v in data.items() if v is not None}.items()
            )
        ]

    def _pck_form_header(self, metadata: SurveyMetadata) -> str:
        """Generate a form header for PCK data."""
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        ru_check: str = ru[-1] if ru and ru[-1].isalpha() else ""
        period: str = self.convert_period(metadata["period_id"])
        form_type: str = metadata["form_type"]

        return f"{form_type}:{ru_ref}{ru_check}:{period}"

    def _pck_item(self, q: int, a: int) -> str:
        """Return a PCK line item."""
        if a < 0:
            # CS can't handle negative numbers!
            a = 99999999999
        return "{0:04} {1:011}".format(q, a)


class MBSFormatter(CSFormatter):

    idbr_ref: dict[str, str] = {
        "0106": "T106G",
        "0111": "T111G",
        "0161": "T161G",
        "0117": "T117G",
        "0123": "T123G",
        "0158": "T158G",
        "0167": "T167G",
        "0173": "T173G",
        "0201": "MB01B",
        "0202": "MB01B",
        "0203": "MB03B",
        "0204": "MB03B",
        "0205": "MB15B",
        "0216": "MB15B",
        "0251": "MB51B",
        "0253": "MB53B",
        "0255": "MB65B",
        "0817": "T817G",
        "0823": "T823G",
        "0867": "T867G",
        "0873": "T873G",
    }

    def generate_pck(self, data: dict[str, Value], metadata: SurveyMetadata) -> PCK:
        """Write a PCK file."""
        m: SurveyMetadata = metadata.copy()
        m["form_type"] = self.idbr_ref.get(metadata["form_type"])
        return super().generate_pck(data, m)

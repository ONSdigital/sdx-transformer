from typing import Optional

from app.definitions.data import SurveyMetadata, Empty, Value
from app.services.formatters.formatter import Formatter


def _get_scan_number(metadata: SurveyMetadata, ref: Optional[str] = None) -> str:
    """Create a scan number based on the passed reference.
    If no reference is passed (as should be the case for the top level ru) then
    create a unique number from the ruref, survey_id and period"""
    if ref:
        if ref[0] == "N":
            return f's_{metadata["ru_ref"]}_{metadata["survey_id"]}_{metadata["period_id"]}_{ref}'
        return f's{ref}'

    return f's_{metadata["ru_ref"]}_{metadata["survey_id"]}_{metadata["period_id"]}'


class IDBRFormatter(Formatter):
    """
    Formatter for IDBR systems
    Headers: ruref, checklet, luref, checklet, surveycode, period, formtype, pageno, scanno, batchno,
            qcode, qvalue
    """
    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata, ref: Optional[str] = None) -> list[str]:
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        checklet: str = ru[-1] if ru[-1].isalpha() else ""
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]
        form_type = metadata["form_type"]
        lu_ref = ref if ref else "00000000"
        lu_checklet = "A"
        page_no = "001"
        scan_no = _get_scan_number(metadata, ref)

        line_list = []
        for qcode, value in sorted(data.items()):

            if str(qcode)[0].isalpha():
                qcode = str(qcode)[1:]

            if value is Empty:
                continue

            line_list.append(f"{ru_ref}^{checklet}^{lu_ref}^"
                             f"{lu_checklet}^{survey_id}^{period}^{form_type}^{page_no}^{scan_no}^^{qcode}^{value}\r")

        return sorted(line_list)

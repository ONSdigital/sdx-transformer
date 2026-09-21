from typing import Optional

from app.definitions.input import Empty, Value
from app.services.formatters.formatter import _SurveyMetadata
from app.services.formatters.pck_formatter import PckFormatter


def _get_scan_number(metadata: _SurveyMetadata, ref: Optional[str] = None) -> str:
    """Create a scan number based on the passed reference.
    If no reference is passed (as should be the case for the top level ru) then
    create a unique number from the ruref, survey_id and period"""
    if ref and ref != "0":
        if ref[0] == "N":
            return f's_{metadata.ru_ref}_{metadata.survey_id}_{metadata.period_id}_{ref}'
        return f's{ref}'

    return f's_{metadata.ru_ref}_{metadata.survey_id}_{metadata.period_id}'


class IdbrFormatter(PckFormatter):
    """
    Formatter for IDBR systems
    Headers: ruref, checklet, luref, checklet, surveycode, period, formtype, pageno, scanno, batchno,
            qcode, qvalue
    """
    def prepare_instance(self, instance: str, data: dict[str, Value]) -> dict[str, Value]:
        sorted_data = dict(sorted({k: v for k, v in data.items() if v is not None}.items(),
                key=lambda x: x[0][1:]
        ))

        return sorted_data

    def convert_value(self, qcode: str, value: str, instance: str, metadata: _SurveyMetadata) -> str:
        ru: str = metadata.ru_ref
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        checklet: str = ru[-1] if ru[-1].isalpha() else ""
        period: str = metadata.period_id
        survey_id = metadata.survey_id
        form_type = metadata.form_type
        lu_ref = instance if instance != "0" else "00000000"  # ?
        lu_checklet = "A"
        page_no = "001"
        scan_no = _get_scan_number(metadata, instance)

        if str(qcode)[0].isalpha():
            qcode = str(qcode)[1:]

        if value is Empty:
            return ""

        return f"{ru_ref}^{checklet}^{lu_ref}^{lu_checklet}^{survey_id}^{period}^{form_type}^{page_no}^{scan_no}^^{qcode}^{value}\r"

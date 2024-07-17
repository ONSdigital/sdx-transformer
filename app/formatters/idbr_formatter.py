from app.definitions import Value, SurveyMetadata, Empty
from app.formatters.formatter import Formatter


class IDBRFormatter(Formatter):
    """
    Formatter for IDBR systems
    Headers: ruref, checklet, luref, checklet, surveycode, period, formtype, pageno, scanno, batchno,
            qcode, qvalue

            cant provide  pageno, scanno
            set these to fixed values

            luref checklet, batchno can be left blank

    """
    def _pck_lines(self, data: dict[str, Value], metadata: SurveyMetadata) -> list[str]:
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        checklet: str = ru[-1] if ru[-1].isalpha() else ""
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]
        form_type = metadata["form_type"]
        lu_ref = "00000000"
        page_no = "001"

        line_list = []
        for qcode, value in sorted(data.items()):

            if str(qcode)[-1].isalpha():
                qcode = str(value)[:-1]

            value = value if value is not Empty else ''

            line_list.append(f"{ru_ref}^{checklet}^{lu_ref}^{survey_id}^{period}^{form_type}^{page_no}^^^{qcode}^{value}")

        return line_list


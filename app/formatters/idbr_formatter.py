from app.definitions import Value, SurveyMetadata
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






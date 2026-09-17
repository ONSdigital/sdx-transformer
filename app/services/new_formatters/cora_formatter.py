from app.definitions.input import SurveyMetadata, Empty
from app.definitions.spec import BuildSpec
from app.services.new_formatters.pck_formatter import PckFormatter


class CORAFormatter(PckFormatter):
    """
    Formatter for CORA systems.
    """
    def __init__(self, spec: BuildSpec, metadata: SurveyMetadata):
        super().__init__(spec, metadata)
        self.page: str = "1"
        self.instance: str = "0"

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SurveyMetadata) -> str:
        ru: str = metadata["ru_ref"]
        ru_ref: str = ru[0:-1] if ru[-1].isalpha() else ru
        period: str = metadata["period_id"]
        survey_id = metadata["survey_id"]
        return f"{survey_id}:{ru_ref}:{self.page}:{period}:{self.instance}:{qcode}:{value if value is not Empty else ''}"


class MESFormatter(CORAFormatter):

    def __init__(self, spec: BuildSpec, metadata: SurveyMetadata):
        super().__init__(spec, metadata)
        self.page: str = "1"
        self.instance: str = "00000"

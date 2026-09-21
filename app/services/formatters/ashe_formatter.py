from app.definitions.input import Value
from app.services.formatters.formatter import SubmissionMetadata
from app.services.formatters.pck_formatter import PckFormatter


class AsheFormatter(PckFormatter):

    def __init__(self, metadata: SubmissionMetadata):
        super().__init__(metadata)
        self._instance_ids: list[str] = []

    def prepare_instance(self, instance: str, data: dict[str, Value]) -> dict[str, Value]:
        sorted_data = dict(sorted({k: v for k, v in data.items() if v is not None}.items(),
                key=lambda x: x[0][1:]
        ))

        if instance not in self._instance_ids:
            self._instance_ids.append(instance)

        return sorted_data

    def _sub_header(self, instance: str, metadata: SubmissionMetadata) -> str:
        """Generate a sub header for PCK data."""
        nino = instance
        period = metadata.period_id
        return f'FV\nHE{period}:{nino}:{period}'

    def convert_value(self, qcode: str, value: str, instance: str, metadata: SubmissionMetadata) -> str:
        line: str = self._get_value(qcode, value)
        if instance in self._instance_ids:
            # ensure header is written only once for each new instance
            self._instance_ids.remove(instance)
            header = self._sub_header(instance, metadata)
            return f'{header}\n{line}'
        else:
            return line

    def _get_value(self, qcode: str, value: str) -> str:
        if qcode.isdigit():
            q = int(qcode)
            if value.isdigit():
                v = int(value)
                if v < 0:
                    # CS can't handle negative numbers!
                    v = 99999999999
                return "{0:04} {1:011}".format(q, v)
            else:
                return "{0:04} {1}".format(q, value)
        else:
            return f"{qcode} {value}"

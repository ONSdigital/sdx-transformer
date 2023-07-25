import json

from app.definitions import SubmissionJson
from app.formatters.formatter import Formatter


class TestFormatter(Formatter):

    def generate_pck(self) -> str:
        return json.dumps({str(int(k)): v for k, v in self._data.items() if v is not None})


def read_submission(filepath: str) -> SubmissionJson:
    with open(filepath) as f:
        submission_json: SubmissionJson = json.load(f)

    return submission_json

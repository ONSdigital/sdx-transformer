from dataclasses import dataclass

from app.definitions.input import Field

iso_8601_date = str  # YYYY-MM-DD


@dataclass
class Answer:
    qcode: str
    value: Field
    instance: str


@dataclass
class Submission:
    tx_id: str
    survey_id: str
    period_id: str
    ru_ref: str
    form_type: str
    case_id: str
    receipt_id: str
    submitted_at: str
    additional: dict[str, Field]
    answers: list[Answer]
    supplementary: dict[str, list[dict[str, str]]]

    def find_answers(self, qcode: str) -> list[Answer]:
        return [answer for answer in self.answers if answer.qcode == qcode]

    def exists(self, qcode: str) -> bool:
        return len(self.find_answers(qcode)) > 0

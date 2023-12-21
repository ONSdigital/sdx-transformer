from dataclasses import dataclass


@dataclass(order=True)
class Answer:
    qcode: str
    value: str | None
    list_item_id: str | None
    group: str | None


@dataclass(order=True)
class SPP:
    questioncode: str
    response: str | None
    instance: int

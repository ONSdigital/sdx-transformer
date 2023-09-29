import json

from app.definitions import ListCollector, Data


def read_submission_data(filepath: str) -> ListCollector:
    with open(filepath) as f:
        submission_data: Data = json.load(f)

    return submission_data

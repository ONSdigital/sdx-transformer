import json

from app.definitions import Data, Empty


def read_submission_data(filepath: str) -> Data:
    with open(filepath) as f:
        submission_data: Data = json.load(f)

    return submission_data


def remove_empties(data: dict[str, str | Empty]) -> Data:
    return {k: v for k, v in data.items() if v is not Empty}

import json

from app.definitions import Data, Empty, PCK


def read_submission_data(filepath: str) -> Data:
    with open(filepath) as f:
        submission_data: Data = json.load(f)

    return submission_data


def remove_empties(data: dict[str, str | Empty]) -> Data:
    return {k: v for k, v in data.items() if v is not Empty}


def convert_pck_to_dict(pck: PCK) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in pck.split("\n"):
        x = line.split(" ")
        k = x[0].strip()
        if len(x) > 1:
            v = x[1].strip()
            result[k] = v
        elif k != "":
            result[k] = ""

    return result

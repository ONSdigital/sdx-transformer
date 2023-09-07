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
        chunks: list[str] = line.split(" ")
        key = chunks[0].strip()
        if len(chunks) > 1:
            v: str = chunks[1].strip()
            result[key] = v
        elif key != "":
            items: list[str] = key.split(":")
            item_count: int = len(items)
            if item_count > 1:
                result[":".join(items[0:item_count-1])] = items[item_count-1]
            else:
                result[key] = ""

    return result


def are_equal(expected: PCK, actual: PCK) -> bool:
    exp: dict[str, str] = convert_pck_to_dict(expected)
    act: dict[str, str] = convert_pck_to_dict(actual)

    print("-----------------")
    equal = True
    for k, v in exp.items():
        if k not in act:
            equal = False
            print(f"Expected key {k} not found in Actual")
        else:
            x = act[k]
            if x != v:
                equal = False
                print(f"Actual value {x} != {v} for key {k}")

    for k in act.keys():
        if k not in exp:
            equal = False
            print(f"Not expecting key {k}")

    return equal

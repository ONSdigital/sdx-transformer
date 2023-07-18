from app.definitions import Field, Empty


def _all_empty(*fields: Field) -> bool:
    for f in fields:
        if isinstance(f, dict):
            for x in f.values():
                if x is not Empty:
                    return False
        if isinstance(f, list):
            for x in f:
                if x is not Empty:
                    return False
        else:
            if f is not Empty:
                return False
    return True

from app.definitions import Value
from app.functions.numerical import round_half_up, divide


def currency_thousands(value: Value) -> Value:
    v = round_half_up(value, nearest="1000")
    val = divide(v, by="1000")
    return "0" if val == "-0" else val
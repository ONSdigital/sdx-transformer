from collections.abc import Callable

from app.services.transform.functions.compound import currency_thousands, period_start, period_end
from app.services.transform.functions.general import no_transform, exists, any_exists, lookup
from app.services.transform.functions.lists import as_list, append_to_list, prepend_to_list, trim_list
from app.services.transform.functions.numerical import round_half_up, aggregate, mean, number_equals, total, divide
from app.services.transform.functions.string import (starts_with, contains, any_contains,
                                                     concat, carve, string_padding,
                                                     space_split, postcode_start, postcode_end, whitespace_removal)
from app.services.transform.functions.time import (to_date, any_date, start_of_month,
                                                   end_of_month, start_of_year, end_of_year, month_year_string)

_function_lookup: dict[str, Callable] = {
    "VALUE": no_transform,
    "EXISTS": exists,
    "ANY_EXISTS": any_exists,
    "LOOKUP": lookup,
    "STARTS_WITH": starts_with,
    "CONTAINS": contains,
    "ANY_CONTAINS": any_contains,
    "CONCAT": concat,
    "TO_DATE": to_date,
    "ANY_DATE": any_date,
    "START_OF_MONTH": start_of_month,
    "END_OF_MONTH": end_of_month,
    "START_OF_YEAR": start_of_year,
    "END_OF_YEAR": end_of_year,
    "MONTH_YEAR_STRING": month_year_string,
    "ROUND": round_half_up,
    "TOTAL": total,
    "DIVIDE": divide,
    "AGGREGATE": aggregate,
    "MEAN": mean,
    "NUMBER_EQUALS": number_equals,
    "CURRENCY_THOUSANDS": currency_thousands,
    "PERIOD_START": period_start,
    "PERIOD_END": period_end,
    "CARVE": carve,
    "AS_LIST": as_list,
    "APPEND_TO_LIST": append_to_list,
    "PREPEND_TO_LIST": prepend_to_list,
    "TRIM_LIST": trim_list,
    "PADDING": string_padding,
    "SPACE_SPLIT": space_split,
    "POSTCODE_START": postcode_start,
    "POSTCODE_END": postcode_end,
    "WHITESPACE_REMOVAL": whitespace_removal,
}

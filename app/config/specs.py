from app.definitions.input import SurveyMetadata
from app.definitions.mapper import Selector
from app.services.mappers.spec_selectors import BuildSpecSelector, PrepopSelector


_build_spec_mapping: dict[str, Selector[SurveyMetadata, str]] = {
        "001": BuildSpecSelector("looping"),
        "009": BuildSpecSelector("mbs"),
        "017": BuildSpecSelector("stocks"),
        "019": BuildSpecSelector("qcas"),
        "024": BuildSpecSelector("fuels"),
        "061": BuildSpecSelector("sppi"),
        "066": BuildSpecSelector("qsl"),
        "068": BuildSpecSelector("qrt"),
        "071": BuildSpecSelector("qs"),
        "073": BuildSpecSelector("blocks"),
        "074": BuildSpecSelector("bricks"),
        "076": BuildSpecSelector("qsm"),
        "092": BuildSpecSelector("mes"),
        "127": BuildSpecSelector("mcg"),
        "132": BuildSpecSelector("ppi"),
        "134": BuildSpecSelector("mwss"),
        "139": BuildSpecSelector("qbs"),
        "144": BuildSpecSelector("ukis"),
        "160": BuildSpecSelector("qpses"),
        "165": BuildSpecSelector("qpsespb"),
        "169": BuildSpecSelector("qpsesrap"),
        "171": BuildSpecSelector("acas"),
        "182": BuildSpecSelector("vacancies"),
        "183": BuildSpecSelector("vacancies"),
        "184": BuildSpecSelector("vacancies"),
        "185": BuildSpecSelector("vacancies"),
        "187": BuildSpecSelector("des"),
        "194": BuildSpecSelector("rails"),
        "202": BuildSpecSelector("abs"),
        "221": BuildSpecSelector("bres"),
        "228": BuildSpecSelector("construction"),
        "999": BuildSpecSelector("looping-spp"),
}

_spp_spec_mapping: dict[str, Selector[SurveyMetadata, str]] = {
    "002": BuildSpecSelector("berd"),
    "009": BuildSpecSelector("mbs-spp"),
    "023": BuildSpecSelector("rsi-spp"),
    "139": BuildSpecSelector("qbs-spp"),
    "228": BuildSpecSelector("construction-spp"),
}


_prepop_spec_mapping: dict[str, Selector[str, str]] = {
    "066": PrepopSelector("land-prepop"),
    "068": PrepopSelector("tiles-prepop"),
    "061": PrepopSelector("sppi-prepop"),
    "071": PrepopSelector("slate-prepop"),
    "076": PrepopSelector("marine-prepop"),
    "132": PrepopSelector("prices-prepop"),
    "221": PrepopSelector("bres-prepop"),
    "241": PrepopSelector("brs-prepop"),
}

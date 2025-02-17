from app.definitions.data import SurveyMetadata
from app.definitions.mapper import Selector
from app.mappers.spec_selectors import BuildSpecSelector, BuildSpecPeriodSelector, PrepopSelector


_build_spec_mapping: dict[str, Selector[SurveyMetadata, str]] = {
        "001": BuildSpecSelector("looping"),
        "002": BuildSpecSelector("berd"),
        "009": BuildSpecPeriodSelector(period_id="2503", before="mbs", after_or_equal="mbs-spp"),
        "017": BuildSpecSelector("stocks"),
        "019": BuildSpecSelector("qcas"),
        "024": BuildSpecSelector("fuels"),
        "066": BuildSpecSelector("qsl"),
        "068": BuildSpecSelector("qrt"),
        "071": BuildSpecSelector("qs"),
        "073": BuildSpecSelector("blocks"),
        "074": BuildSpecSelector("bricks"),
        "076": BuildSpecSelector("qsm"),
        "092": BuildSpecSelector("mes"),
        "127": BuildSpecSelector("mcg"),
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


_prepop_spec_mapping: dict[str, Selector[str, str]] = {
    "066": PrepopSelector("land-prepop"),
    "068": PrepopSelector("tiles-prepop"),
    "071": PrepopSelector("slate-prepop"),
    "076": PrepopSelector("marine-prepop"),
    "221": PrepopSelector("bres-prepop"),
    "241": PrepopSelector("brs-prepop"),
}

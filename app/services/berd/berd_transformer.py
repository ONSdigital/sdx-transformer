import json
from dataclasses import asdict

from sdx_gcp.app import get_logger

from app.services.berd.collect_items import collect_list_items
from app.services.berd.convert_data import extract_answers, convert_to_spp, convert_civil_defence, remove_prepend_values
from app.services.berd.definitions import SPP
from app.definitions.data import SurveyMetadata, ListCollector, PCK, SPP as SppResult

logger = get_logger()


def berd_to_spp(list_data: ListCollector, survey_metadata: SurveyMetadata) -> PCK:
    berd_data: list[SPP] = convert_to_spp(collect_list_items(extract_answers(list_data)))
    berd_data_list: list[dict[str, str | int]] = [asdict(d) for d in berd_data]
    # the SPP file should not contain prepended values and requires a transform for civil & defence
    data = remove_prepend_values(convert_civil_defence(berd_data_list))

    ru_ref = survey_metadata["ru_ref"]

    spp: SppResult = {
        "formtype": survey_metadata["form_type"],
        "reference": ru_ref[0:-1] if ru_ref[-1].isalpha() else ru_ref,
        "period": survey_metadata["period_id"],
        "survey": survey_metadata["survey_id"],
        "responses": data,
    }

    return json.dumps(spp)


def berd_to_image(list_data: ListCollector, _survey_metadata: SurveyMetadata) -> PCK:
    berd_data: list[SPP] = convert_to_spp(collect_list_items(extract_answers(list_data)))
    berd_data_list: list[dict[str, str | int]] = [asdict(d) for d in berd_data]
    return json.dumps(berd_data_list)

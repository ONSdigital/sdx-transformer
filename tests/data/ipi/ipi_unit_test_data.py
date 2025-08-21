from app.definitions.input import SurveyMetadata, ListCollector

survey_metadata: SurveyMetadata = {
    "survey_id": "156",
    "period_id": "201605",
    "ru_ref": "23456789012",
    "form_type": "0001",
    "period_start_date": "2016-05-01",
    "period_end_date": "2016-05-31",
}

original_data: ListCollector = {
    "answers": [
        {
            "answer_id": "answerc7fcba68-57cc-4b8c-9842-ea049341290f",
            "value": "0"
        },
        {
            "answer_id": "answer56fdc60f-cd07-49bf-9d28-961202ef0835",
            "value": 100
        },
        {
            "answer_id": "answera51328d4-9b19-468a-bebe-6030ce6238c4",
            "value": "Item comment 1"
        },
        {
            "answer_id": "answere237201d-a281-4228-a538-85e93ada4263",
            "value": "Overall comment"
        }
    ],
    "lists": [],
    "answer_codes": [
        {
            "answer_id": "answerc7fcba68-57cc-4b8c-9842-ea049341290f",
            "code": "9999"
        },
        {
            "answer_id": "answer56fdc60f-cd07-49bf-9d28-961202ef0835",
            "code": "9997"
        },
        {
            "answer_id": "answera51328d4-9b19-468a-bebe-6030ce6238c4",
            "code": "9996"
        },
        {
            "answer_id": "answere237201d-a281-4228-a538-85e93ada4263",
            "code": "9995"
        }
    ]
}

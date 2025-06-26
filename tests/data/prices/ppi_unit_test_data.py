from app.definitions.input import SurveyMetadata, ListCollector

survey_metadata: SurveyMetadata = {
    "survey_id": "132",
    "period_id": "201605",
    "ru_ref": "23456789012",
    "form_type": "0001",
    "period_start_date": "2016-05-01",
    "period_end_date": "2016-05-31",
}

original_data: ListCollector = {
    "answers": [
        {
            "answer_id": "answer79616595-fc1e-41c5-9b28-ccd1b92d591e",
            "value": "0",
            "list_item_id": "uVlxJv"
        },
        {
            "answer_id": "answerf588e908-9671-492c-ac3c-b94f5b5d1db7",
            "value": 200,
            "list_item_id": "uVlxJv"
        },
        {
            "answer_id": "answer231f0980-1bed-4b42-867b-af7be48075c9",
            "value": "This is a figure comment",
            "list_item_id": "uVlxJv"
        },
        {
            "answer_id": "answer79616595-fc1e-41c5-9b28-ccd1b92d591e",
            "value": "0",
            "list_item_id": "RiupLc"
        },
        {
            "answer_id": "answerf588e908-9671-492c-ac3c-b94f5b5d1db7",
            "value": 400,
            "list_item_id": "RiupLc"
        },
        {
            "answer_id": "answer231f0980-1bed-4b42-867b-af7be48075c9",
            "value": "This is another figure comment",
            "list_item_id": "RiupLc"
        },
        {
            "answer_id": "answerec27606d-a18b-4148-823c-54e0683ae6ff",
            "value": "This is the general survey comment"
        }
    ],
    "lists": [
        {
            "items": [
                "uVlxJv",
                "RiupLc"
            ],
            "name": "item",
            "supplementary_data_mappings": [
                {
                    "identifier": "12345678901",
                    "list_item_id": "uVlxJv"
                },
                {
                    "identifier": "98765432101",
                    "list_item_id": "RiupLc"
                }
            ]
        }
    ],
    "answer_codes": [
        {
            "answer_id": "answer79616595-fc1e-41c5-9b28-ccd1b92d591e",
            "code": "9999"
        },
        {
            "answer_id": "answerf588e908-9671-492c-ac3c-b94f5b5d1db7",
            "code": "9997"
        },
        {
            "answer_id": "answer231f0980-1bed-4b42-867b-af7be48075c9",
            "code": "9996"
        },
        {
            "answer_id": "answerec27606d-a18b-4148-823c-54e0683ae6ff",
            "code": "9995"
        }
    ]
}

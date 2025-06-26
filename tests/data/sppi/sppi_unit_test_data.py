from app.definitions.input import SurveyMetadata, ListCollector

survey_metadata: SurveyMetadata = {
    "survey_id": "061",
    "period_id": "201605",
    "ru_ref": "23456789012",
    "form_type": "0011",
    "period_start_date": "2016-05-01",
    "period_end_date": "2016-05-31",
}

original_data: ListCollector = {
    "answers": [
      {
        "answer_id": "answera6755e2f-9a3c-4031-83aa-2c4f00813c5f",
        "value": "0",
        "list_item_id": "TJmMsG"
      },
      {
        "answer_id": "answerba95f3c0-9784-496c-99fe-b8f9faa5a772",
        "value": 1000,
        "list_item_id": "TJmMsG"
      },
      {
        "answer_id": "answerec475dd4-cccc-43c3-a8d8-71d26eafe438",
        "value": "Comment for 1000 cost product",
        "list_item_id": "TJmMsG"
      },
      {
        "answer_id": "answera6755e2f-9a3c-4031-83aa-2c4f00813c5f",
        "value": "0",
        "list_item_id": "RZCIdC"
      },
      {
        "answer_id": "answerba95f3c0-9784-496c-99fe-b8f9faa5a772",
        "value": 2000,
        "list_item_id": "RZCIdC"
      },
      {
        "answer_id": "answerec475dd4-cccc-43c3-a8d8-71d26eafe438",
        "value": "Comment for 2000 product",
        "list_item_id": "RZCIdC"
      },
      {
        "answer_id": "answer095ebfb4-a16b-45da-8f61-b0a85ae48262",
        "value": "Overall comment"
      }
    ],
    "lists": [
      {
        "items": [
          "TJmMsG",
          "RZCIdC"
        ],
        "name": "service",
        "supplementary_data_mappings": [
          {
            "identifier": "7732015057",
            "list_item_id": "TJmMsG"
          },
          {
            "identifier": "7732016043",
            "list_item_id": "RZCIdC"
          }
        ]
      }
    ],
    "answer_codes": [
      {
        "answer_id": "answera6755e2f-9a3c-4031-83aa-2c4f00813c5f",
        "code": "9999"
      },
      {
        "answer_id": "answerba95f3c0-9784-496c-99fe-b8f9faa5a772",
        "code": "9997"
      },
      {
        "answer_id": "answerec475dd4-cccc-43c3-a8d8-71d26eafe438",
        "code": "9996"
      },
      {
        "answer_id": "answer095ebfb4-a16b-45da-8f61-b0a85ae48262",
        "code": "9995"
      }
    ]
 }

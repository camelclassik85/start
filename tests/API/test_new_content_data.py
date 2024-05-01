import allure
from jsonschema import validate
from start.api.api import api_call
from start.constants import ApiUrl
from start.schemas.new_content_data_schema import new_content


@allure.epic('API tests')
@allure.feature('New content data')
@allure.story("Checking new content data")
def test_search_one_item_result_data_api():
    endpoint = "/categories"
    params = {"category": "movie,series",
              "device_type": "web",
              "sort": "-start_release_date",
              "apikey": "a20b12b279f744f2b3c7b5c5400c4eb5",
              "locale": "ru",
              "content_lang": "ru",
              "limit": 20,
              "skip": 0
              }

    response = api_call.api_request(ApiUrl.base_api_url, endpoint, "GET", params=params)

    with allure.step('Check status code = 200'):
        assert response.status_code == 200
    with allure.step(f'Check items total more than 0'):
        assert response.json()['items_total'] > 0
    if response.json()['items_total'] > 20:
        with allure.step(f'Check 20 items limit in response'):
            assert len(response.json()['items']) == 20
    with allure.step('Validate Schema'):
        validate(response.json(), new_content)

import allure
from jsonschema import validate
from start_project_tests.api.api import api_call
from start_project_tests.test_data.constants import ApiUrl
from start_project_tests.test_data.content import cheburashka, chyornaya_vesna
from start_project_tests.test_data.users import authorized_user
from start_project_tests.schemas.favorites_data_schema import favorites_schema


@allure.epic('API tests')
@allure.feature('Favorites data')
@allure.story("Checking GET favorites data")
def test_get_favorites_data_api():
    with allure.step("Add content to favorites"):
        api_call.add_to_favorites(user=authorized_user, content_uid=cheburashka.uid)
        api_call.add_to_favorites(user=authorized_user, content_uid=chyornaya_vesna.uid)

    endpoint = "/profile/favorites/" + authorized_user.default_profile_id
    params = {"apikey": "a20b12b279f744f2b3c7b5c5400c4eb5",
              "locale": "ru",
              "content_lang": "ru"
              }
    cookies = {'auth': authorized_user.auth}
    response = api_call.api_request(ApiUrl.base_api_url, endpoint, "GET", params=params, cookies=cookies)

    with allure.step('Check status code = 200'):
        assert response.status_code == 200
    with allure.step('Check favorites q-ty'):
        assert len(response.json()) == 2
    with allure.step('Check 1st item alias in list'):
        assert response.json()[0]['alias'] == chyornaya_vesna.alias
    with allure.step('Check 2nd item alias in list'):
        assert response.json()[1]['alias'] == cheburashka.alias
    with allure.step('Validate Schema'):
        validate(response.json(), favorites_schema)

    with allure.step("Delete content from favorites"):
        api_call.delete_from_favorites(user=authorized_user, content_uid=cheburashka.uid)
        api_call.delete_from_favorites(user=authorized_user, content_uid=chyornaya_vesna.uid)

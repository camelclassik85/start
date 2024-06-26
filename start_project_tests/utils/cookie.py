from selene import browser
from start_project_tests.test_data.constants import web_base_url
from start_project_tests.test_data.users import User


def add_auth_cookie_to_browser(user: User, url: str = '/'):
    browser.config.base_url = ''
    browser.open('https://api.start.ru/')
    browser.driver.add_cookie({
        "name": "auth",
        "value": user.auth,
        "HttpOnly": True,
        "Secure": True,
        "SameSite": None})
    browser.open(web_base_url + url)

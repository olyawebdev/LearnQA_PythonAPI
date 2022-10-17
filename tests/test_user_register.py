import time

import pytest as pytest
import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    @allure.title("Positive registration test")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        URI = "/user/"
        data = self.prepare_registration_data()
        response = MyRequests.post(URI, data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Registration with existing email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        URI = "/user/"
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(URI, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            self.ERRORS["response.content"].format(response.content)

    @allure.title("Registration, email without @")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_invalid_email(self):
        URI = "/user/"
        email = 'nameexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(URI, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            self.ERRORS["response.content"].format(response.content)

    @allure.title("The field {field} is absent while registration")
    @pytest.mark.parametrize(
        'field', ['password', 'username', 'firstName', 'lastName', 'email']
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_without_one_field(self, field):
        URI = "/user/"
        data = self.prepare_registration_data()
        data.pop(field)
        print(data)
        response = MyRequests.post(URI, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}", \
            self.ERRORS["response.content"].format(response.content)

    @allure.title("Registration with very short or very long name")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        'name', ['a',
                 'AkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakiyAkakk'
                 # 251 символ
                 ]
    )
    def test_create_user_long_or_short_name(self, name):
        time.sleep(1)
        URI = "/user/"
        data = self.prepare_registration_data()
        data["name"] = name
        print(data)
        response = MyRequests.post(URI, data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

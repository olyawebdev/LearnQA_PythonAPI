from datetime import datetime

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        URI = "/user/"
        data = self.prepare_registration_data()
        response = MyRequests.post(URI, data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        URI = "/user/"
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post(URI, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists",\
            self.ERRORS["response.content"].format(response.content)


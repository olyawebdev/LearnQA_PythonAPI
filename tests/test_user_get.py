'''
На занятиях в классе TestUserGet мы писали тест на запрос, показывающий данные пользователя. Мы покрыли тестами два кейса:


- неавторизованный запрос на данные - там мы получили только username

- авторизованный запрос - мы были авторизованы пользователем с ID 2 и делали запрос для получения данных того же пользователя, в этом случае мы получали все поля


В этой задаче нужно написать тест, который авторизовывается одним пользователем, но получает данные другого (т.е. с другим ID). И убедиться, что в этом случае запрос также получает только username, так как мы не должны видеть остальные данные чужого пользователя.
'''

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")

        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_detais_auth_as_same_user(self):
        URI_login = "/user/login"
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post(URI_login, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_detais_auth_as_another_user(self):
        URI_login = "/user/login"
        data = {
            'email': 'learnqa10122022152859@example.com',
            'password': '123'
        }

        response1 = MyRequests.post(URI_login, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        test_user_id = 2
        assert user_id_from_auth_method != test_user_id

        response2 = MyRequests.get(
            f"/user/{test_user_id}", #ID другой, не моего юзера
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username"]
        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)
        Assertions.assert_json_has_not_keys(response2, unexpected_fields)

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):

    def setup(self):
        self.URI_login = "/user/login"
        self.URI_user = "/user/"

    def register_new_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post(
            self.URI_user,
            data=register_data
        )
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")
        return email, password, user_id

    def login(self, email, password):
        # LOGIN

        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post(
            self.URI_login,
            data=login_data
        )
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        return auth_sid, token

    def test_delete_my_user(self):
        email, password, user_id = self.register_new_user()
        auth_sid, token = self.login(email, password)

        #DELETE
        response1 = MyRequests.delete(
            url=self.URI_user+str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response1, 200)

        #GET
        response2 = MyRequests.get(
            self.URI_user + str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response2, 404)

    def test_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        auth_sid, token = self.login(data["email"], data["password"])
        response = MyRequests.delete(
            url=self.URI_user+str(2),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response, 400)
        assert response.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5."

    def test_delete_another_user(self):
        email, password, user_id = self.register_new_user()
        auth_sid, token = self.login(email, password)

        another_user_id = 45183

        #DELETE
        response1 = MyRequests.delete(
            url=self.URI_user+str(another_user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        #Здесь получили 200, но следующий GET запрос показывает, что пользователь не удалён

        #GET
        response2 = MyRequests.get(
            self.URI_user + str(another_user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "username")





'''
У нас есть метод, который удаляет пользователя по ID - DELETE-метод https://playground.learnqa.ru/api/user/{id}


Само собой, удалить можно только того пользователя, из-под которого вы авторизованы.


Необходимо в директории tests/ создать новый файл test_user_delete.py с классом TestUserDelete.


Там написать следующие тесты.


Первый - на попытку удалить пользователя по ID 2. Его данные для авторизации:


        data = {

            'email': 'vinkotov@example.com',

            'password': '1234'

        }



Убедиться, что система не даст вам удалить этого пользователя.



Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.


Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.

==========================================
'''

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

        #GET
        response1 = MyRequests.get(
            self.URI_user + str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        Assertions.assert_json_has_keys(response1, ["username", "email", "firstName", "lastName"])

        #DELETE
        data = {
            "password": password,
            "username": self.get_json_value(response1, "username"),
            "firstName": self.get_json_value(response1, "firstName"),
            "lastName": self.get_json_value(response1, "lastName"),
            "email": self.get_json_value(response1, "email")
        }
        response2 = MyRequests.delete(
            url=self.URI_user+str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data=data
        )
        Assertions.assert_code_status(response2, 200)




import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):

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

    @allure.title("Edit just created user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_just_created_user(self):

        email, password, user_id = self.register_new_user()

        auth_sid, token = self.login(email, password)

        #EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(
            self.URI_user+str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = MyRequests.get(
            self.URI_user + str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.title("Edit user without auth")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_no_auth(self):
        #EDIT
        user_id = 44692
        new_name = "Changed Name"
        response3 = MyRequests.put(
            self.URI_user+str(user_id),
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 400)

    @allure.title("Edit another user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_another_user(self):
        email, password, user_id = self.register_new_user()
        auth_sid, token = self.login(email, password) #Авторизовались под только что созданным юзером
        user_id_to_edit = 45167 #Этого пытаемся изменить
        new_firstName = "Masha"
        response1 = MyRequests.put(
            self.URI_user+str(user_id_to_edit),
            data={"firstName": new_firstName},
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        #Обнаружен баг - получен ответ 200

        #Теперь авторизуемся под 45167, которого пытались поменять и с помощью get проверим, поменялось ли firstName
        email, password = 'learnqa10152022220109@example.com', '123'
        auth_sid, token = self.login(email, password)
        response2 = MyRequests.get(
            self.URI_user+str(user_id_to_edit),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )
        firstName = self.get_json_value(response2, "firstName")
        assert firstName != new_firstName, f"First name of the user {user_id_to_edit} was changed by {user_id}. New name is {new_firstName}."
        #Assert успешно отработал, имя пользователя осталось прежним.

    @allure.title("Edit user's email to invalid")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_user_email_invalid(self):
        email, password, user_id = self.register_new_user()
        auth_sid, token = self.login(email, password)
        new_email = "newemail.com"
        response = MyRequests.put(
            self.URI_user+str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            self.ERRORS["response.content"].format(response.content)

    @allure.title("Edit user's first name to very short (one symbol)")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_edit_user_short_firstname(self):
        email, password, user_id = self.register_new_user()
        auth_sid, token = self.login(email, password)
        response = MyRequests.put(
            self.URI_user+str(user_id),
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": 'q'} #имя из 1 символа
        )

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == '{"error":"Too short value for field firstName"}', \
            self.ERRORS["response.content"].format(response.content)

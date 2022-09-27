import requests

URL = "https://playground.learnqa.ru/api/homework_cookie"


def test_cookie():
    res = requests.get(URL)
    cookie_dict = dict(res.cookies)
    assert cookie_dict
    for k, v in cookie_dict.items():
        print("\nResponse cookies\n{0}:\t{1}".format(k, v))
    assert cookie_dict.get("HomeWork", False), "HomeWork cookie not found"
    assert cookie_dict["HomeWork"] == "hw_value", "HomeWork cookie value not equal to 'hw_value'"

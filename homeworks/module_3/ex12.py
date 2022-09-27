import requests

URL = "https://playground.learnqa.ru/api/homework_header"


def test_header():
    res = requests.get(URL)
    headers_dict = dict(res.headers)
    print("\nResponse headers\n")
    headers_names = ('Date', 'Content-Type', 'Content-Length', 'Connection', 'Keep-Alive', 'Server', 'x-secret-homework-header', 'Cache-Control', 'Expires')
    for k, v in headers_dict.items():
        print("{0}:\t{1}".format(k, v))
        assert k in headers_names, f"Unknown header {k}"
        assert v, f"Header {k} is empty"




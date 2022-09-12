import requests

url = "https://playground.learnqa.ru/api/get_text"
res = requests.get(url)
print(res.text)
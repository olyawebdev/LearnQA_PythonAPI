import requests

url = "https://playground.learnqa.ru/api/long_redirect"
res = requests.get(url)
history = res.history

# Сколько редиректов
print("Redirects counter: {}".format(len(history)))
# URL редиректов
for r in range(len(history)):
    print("Redirect number {0} is {1}".format(r + 1, history[r].url))
# Итоговый URL
print("Final url: {}".format(res.url))

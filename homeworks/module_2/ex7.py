import requests

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = ('POST', 'GET', 'PUT', 'DELETE') #возможные значения параметра
results = dict() #словарь для сохранения результатов


def no_param():
    response = requests.get(URL)
    return response.text


def request_not_in_list():
    response = requests.head(URL)
    return response.text


def valid_methods():
    responses = (
        requests.post(URL, data=dict(method=methods[0])),
        requests.get(URL, params=dict(method=methods[1])),
        requests.put(URL, data=dict(method=methods[2])),
        requests.delete(URL, data=dict(method=methods[3]))
    )
    return responses


def all_methods():
    responses = (
        (requests.get(URL, params=dict(method=m)) for m in methods),
        (requests.post(URL, data=dict(method=m)) for m in methods),
        (requests.put(URL, data=dict(method=m)) for m in methods),
        (requests.delete(URL, params=dict(method=m)) for m in methods)
    )
    return responses


if __name__ == "__main__":
    results[1] = no_param()
    results[2] = request_not_in_list()
    results[3] = [res.text for res in valid_methods()]
    results[4] = [[res.text for res in method] for method in all_methods()]
    print(results)

'''
При запуске вызываются функции, выполняющие каждый пункт задания. Результаты (тела ответов сервера) сохраняются в словарь results. 
При форматировании получившегося словаря как json получился такой результат. Ключ в формате числа - пункт задания.

{
  1: 'Wrong method provided',
  2: '',
  3: [
    '{"success":"!"}',
    '{"success":"!"}',
    '{"success":"!"}',
    '{"success":"!"}'
  ],
  4: [
    [
      'Wrong method provided',
      '{"success":"!"}',
      'Wrong method provided',
      'Wrong method provided'
    ],
    [
      '{"success":"!"}',
      'Wrong method provided',
      'Wrong method provided',
      'Wrong method provided'
    ],
    [
      'Wrong method provided',
      'Wrong method provided',
      '{"success":"!"}',
      'Wrong method provided'
    ],
    [
      'Wrong method provided',
      '{"success":"!"}',
      'Wrong method provided',
      '{"success":"!"}'
    ]
  ]
}

1. Если не передать метод, отдаётся ответ 'Wrong method provided'
2. Если сделать запрос не из списка, отдаст пустую строку
3. С помощью генератора поочерёдно вызвала каждый метод с соответствующим параметром method. Отдан ответ '{"success":"!"}' во всех 4 случаях
4. С помощью вложенных генераторов вызвала каждый метод со всеми 4 возможными параметрами. Если параметр корректный, отдаётся ответ как в п.3, иначе как в п.1. 
Однако, если вызвать метод DELETE с параметром method=get, сервер отвечает успехом. Это, конечно же, неправильное поведение.
'''
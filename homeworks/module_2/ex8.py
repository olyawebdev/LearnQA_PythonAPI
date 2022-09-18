import requests
import json
import time
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG) #прикрутим логи на всякий случай
URL = "https://playground.learnqa.ru/ajax/api/longtime_job"

def token_script():
    logging.info("Script starts")
    #создание задачи
    res = requests.get(URL)
    res_body = json.loads(res.text)
    token = res_body["token"]
    seconds = res_body["seconds"]
    #вызов до готовности задачи
    res = requests.get(URL, params=dict(token=token))
    res_body = json.loads(res.text)
    status = res_body["status"]
    assert status == "Job is NOT ready"
    #ожидание
    time.sleep(seconds)
    #проверка готовности задачи
    res = requests.get(URL, params=dict(token=token))
    res_body = json.loads(res.text)
    try:
        result = res_body["result"]
    except KeyError:
        result = None
    status = res_body["status"]
    assert result, "Job didn't return a result"
    assert status == "Job is ready"


if __name__ == '__main__':
    token_script()
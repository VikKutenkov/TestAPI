# coding: utf-8
import requests
import json

testOK = True

url = 'http://apigw.lamoda.ru/json/get_product_product_recommendations'
print('тест на обязательные поля')
response = requests.post(url)
j_data = json.loads(response.content)
if response.status_code == 400 and 'member must occur at least 1 times' in j_data["faultstring"]:
    print('OK - получили верный ответ с правильной ошибкой:\n', response.status_code, response.reason, j_data)
else:
    print('NG - тест на обязательные поля не пройден\n', response.status_code, response.reason, j_data)
    testOK = False
print()

print('запрос не в json формате')
response = requests.post(url, data={'sku': 'LO019EMJGZ27'})
j_data = json.loads(response.content)
if response.status_code == 400 and 'ValueError' in j_data["faultstring"]:
    print('OK - получили верный ответ с правильной ошибкой:\n', response.status_code, response.reason, j_data)
else:
    print('NG - неверный ответ\n', response.status_code, response.reason, j_data)
    testOK = False
print()

print('проверка условий по-умолчанию - делаем запрос с минимумом данных')
response = requests.post(url,
                         json={'sku': 'LO019EMJGZ27'})
j_data = json.loads(response.content)
""" должны получить 12 вариантов """
if response.status_code == 200 and len(j_data) <= 12:
    print('OK - получили не более 12 вариантов')
elif len(j_data) > 12:
    print('NG - Получили %s ответов, - а должно быть не больше 12' % (len(j_data),))
    testOK = False
print()

print('запрос 2-х рекомендаций')
response = requests.post(url,
                         json={'sku': 'LO019EMJGZ27',
                               'limit': 2})
j_data = json.loads(response.content)
if len(j_data) == 2:
    print('OK - получили 2 варианта:')
    for i in range(len(j_data)):
        print('"product": {"sku": "', j_data[i]["product"]['sku'], '"}')
else:
    print('NG - возвращенное кол-во рекомендаций (%s) не равно запрошенным 2' % (len(j_data),))
    testOK = False
print()

print('запрос некорректного(-1) количества рекомендаций ')
response = requests.post(url,  # headers=headers,
                         json={'sku': 'LO019EMJGZ27',
                               'limit': -1})
j_data = response.json()
if response.status_code == 400:
    print('OK - получили верный ответ:\n', response.status_code, response.reason, j_data)
else:
    print('NG - запрос некорректного(-1) количества рекомендаций выдал не верный ответ\n', response.status_code, response.reason, j_data)
    testOK = False
print()
print()

if testOK is True:
    print('ОК - ТЕСТ ПРОЙДЕН')
else:
    print('ERROR: найдены баги, аварийное завершение теста')
    raise SystemExit  # валим тест. Пиши баг


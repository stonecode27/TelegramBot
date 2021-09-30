import telebot
import requests
import json


class APIException(Exception):  # Класс ошибок бота
    pass


class Values:  # Класс отвечающий за распознавание сообщения и отправку результата
    dict_of_values = {'рубль': 'RUB', 'доллар': 'USD', 'евро': 'EUR',
                      'злотый': 'PLN', 'фунт': 'GBP', 'тенге': 'KZT',
                      'шекель': 'ILS'}

    def check_values(self, message_str: str):  # Метод проверки формата сообщения. Возвращает base, quote, amount
        base = None
        quote = None
        amount = None
        var_list = message_str.lower().split()  # получаем список из сообщения
        if len(var_list) == 3:  # если три элемента в списке
            for i in self.dict_of_values.keys():  # проходимся по всем вариантам валют
                if var_list[0] == i:  # если такая валюта есть
                    base = var_list[0]
                    break
            for i in self.dict_of_values.keys():  # проходимся по всем вариантам валют
                if var_list[1] == i:  # если такая валюта есть
                    quote = var_list[1]
                    break
            if var_list[2].isdigit():
                amount = var_list[2]
            else:
                raise APIException("Неправильный формат сообщения")
        else:
            raise APIException("Неправильный формат сообщения")

        if base and quote and amount and (base != quote):
            return base, quote, amount
        else:
            raise APIException("Неправильный формат сообщения")

    @staticmethod
    def get_price(base, quote, amount):  # Метод, который обращается к апи и считает сумму
        with open("exchangeAK.txt") as f:
            API_TOKEN = f.readline()

        # В связи с ограничениями тарифного плана API будем получать все валюты через евро

        if base == "евро":  # Если собираемся купить евро
            a = requests.get("http://api.exchangeratesapi.io/v1/latest",
                             params={"access_key": API_TOKEN,
                                     "base": "EUR",
                                     "symbols": Values().dict_of_values[quote]})
            b = json.loads(a.content)
            result = float(b["rates"][Values().dict_of_values[quote]]) * float(amount)
            return result
        elif quote == "евро":  # Если собираемся купить за евро
            a = requests.get("http://api.exchangeratesapi.io/v1/latest",
                             params={"access_key": API_TOKEN,
                                     "base": "EUR",
                                     "symbols": "RUB, USD, PLN, GBP, KZT, ILS"})
            b = json.loads(a.content)
            result = float(amount) / (b["rates"][Values().dict_of_values[base]])
            return result

        else:
            a = requests.get("http://api.exchangeratesapi.io/v1/latest",
                             params={"access_key": API_TOKEN,
                                     "base": "EUR",
                                     "symbols": "RUB, USD, PLN, GBP, KZT, ILS"})
            b = json.loads(a.content)
            q_co = float(b["rates"][Values().dict_of_values[quote]])
            b_co = float(b["rates"][Values().dict_of_values[base]])
            result = float(amount)*float(q_co/b_co)
            return result

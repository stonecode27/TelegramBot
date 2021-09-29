import telebot
import requests
import json

class APIException(Exception): # класс ошибок бота
    pass

class Values:
    dict_of_values = {"рубль": "RUB", "доллар": "USD", "евро": "EUR",
                      "злотый": "PLN", "фунт": "GBP", "тенге": "KZT",
                      "шекель": "ILS"}
    def check_values(self, message_str: str):
        counter = 0
        quote = None
        base = None
        if list(filter(str.isdigit, message_str)): # если в строке есть цифры
            amount = int("".join(list(filter(str.isdigit, message_str))))
        else:
            raise APIException("Неправильный формат сообщения")
        a = message_str.lower().split()
        for i in self.dict_of_values:
            for j in a:
                if i == j:
                    counter +=1
                    if counter == 1:
                        quote = i
                    elif counter == 2:
                        base = i
                    else:
                        raise APIException("Неправильный формат сообщения")
        if quote == base:
            raise APIException("Неправильный формат сообщения")

        return quote, base, amount







if __name__ == "__main__":
    a = requests.get("http://api.exchangeratesapi.io/v1/latest", params= {"access_key": "2cc8c7afb1ef15a34285e26c3f7dc582",
                                                                         "base": "EUR", "symbols": "USD"})
    b = json.loads(a.content)
    print(b)


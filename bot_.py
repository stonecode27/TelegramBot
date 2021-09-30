from extensions import *

with open("ttoken.txt") as f:
    TOKEN = f.readline()
    bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"""
Чтобы узнать курс валюты, отправьте сообщение в следующем формате:
<валюта, цену которой хотите узнать> <валюта, которую хотите обменять> <количество желаемой валюты>

Пример: евро рубль 100

Обратите внимание, что количество валюты должно быть целым числом!
Доступные валюты Вы можете посмотреть, отправив команду
/values
""")


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"""
Доступные валюты:
Сокращение - название - команда
RUB - Российский рубль - рубль
USD - США доллар - доллар
EUR - Евро - евро
PLN - Польский злотый - злотый
GBP - Английский фунт - фунт
KZT - Казахский тенге - тенге
ILS - Израильский шекель - шекель 

""")


@bot.message_handler(content_types=['text'])
def price_handler(message: telebot.types.Message):
    try:
        base, quote, amount = Values().check_values(message.text)
        result = Values().get_price(base, quote, amount)
    except APIException as m:
        bot.send_message(message.chat.id, f" Ошибка APIException: {m}")
    else:
        bot.send_message(message.chat.id, f" {amount} {base} будут стоить" + " %.2f " % result +
                         f"{quote}")


if __name__ == "__main__":
    bot.polling(none_stop=True)

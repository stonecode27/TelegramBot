from extensions import *

with open("ttoken.txt") as f:
    TOKEN = f.readline()
    bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"""
Приветствую Вас, {message.chat.username}!

Чтобы узнать курс валюты, отправьте сообщение в следующем формате:
<валюта, цену которой хотите узнать> <валюта, которую хотите обменять> <количество желаемой валюты>

Пример: евро рубль 100
Доступные валюты Вы можете посмотреть, отправив команду /values

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
    quote, base, amount = Values().check_values(message.text)
    bot.send_message(message.chat.id, f"""

Вы хотите купить {amount} {base} в обмен на {quote}

""")


if __name__ == "__main__":
    bot.polling(none_stop=True)


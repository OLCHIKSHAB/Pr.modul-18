import telebot
from config import keys
from extensions import ConvertionException, CryptoConverter
TOKEN = "5856351080:AAFKBnIVx0WRg3rY5Bh-dOyIfwyhmsHB_nU"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def instruction(message: telebot.types.Message):
    text = 'Привет! Я бот! Конвертер валют. \n \
Для рассчета курса валют введите сообщение в формате: \n \n Название валюты, которую будем конвертировать <пробел> \n \
Название валюты, в какую будем конвертировать <пробел> \n \
Количество конвертируемой валюты <пробел> \n \n Пример сообщения: рубль евро 1 \n \n \
Посмотреть список всех доступных валют: /values\n \
Напомнить формат сообщения для расчета курса валют: /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
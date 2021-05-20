import telebot
from config import TOKEN, keys
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Для конвертации валют введите запрос в виде : \n <имя валюты, цену которой вы хотите узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты> \n' \
           'Все доступные валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неправильное количество параметров')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить операцию \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {round((total_base * float(amount)), 5)}'
        bot.send_message(message.chat.id, text)


bot.polling()

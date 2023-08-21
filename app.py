import telebot
from config import keys, TOKEN
from extensions import APIException, MoneyConverter

bot = telebot.TeleBot(TOKEN)


# Обрабатываются сообщения, содержащие команды '/start' or '/help'
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите боту команду в следующем формате:\n'
            '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n'
            'Пример: доллар евро 5\n'
            'Список доступных валют: /values')
    bot.send_message(message.chat.id, text)


# Выводится список всех доступных валют по команде '/values'
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for n, key in enumerate(keys, start=1):
        text = '\n'.join((text, f'{n}) {key[0].upper() + key[1:]}',))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Количество параметров несоответствует запросу')
        quote, base, amount = values
        total_base = MoneyConverter.get_price(quote.lower(), base.lower(), amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка:\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount.lower()} {quote.lower()} в {base}: {round(float(total_base) * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
import telebot
from config import currencies, TOKEN
from extensions import ConvertionException, CryptoConverter


#1. Регистрация бота.
bot = telebot.TeleBot(TOKEN)


#2. Начало работы с ботом (/start и /help).
@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = ("Здравствуй! Чтобы начать работу, введите команду боту в следующем формате:\n\
<Имя валюты> <В какую валюту перевести> <Количество переводимой валюты>\n\n\
Доступные команды: \n\
/values - вывод доступных валют.\n\n\
*Вводите значения строчными буквами через пробел!*")
    bot.send_message(message.chat.id, text)


#3. Вывод пользователю доступных валют (/values).
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, f'– {key}'))
    bot.reply_to(message, text)


#4. Работа с API + Отлов ошибок.
@bot.message_handler(content_types=['text'])
def conversion(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

        if len(values) > 3:
            raise ConvertionException("Слишком много параметров!")
        elif len(values) < 3:
            raise ConvertionException("Недостаточно параметров!")
        elif int(amount) < 1:
            raise ConvertionException("Количество не может быть меньше 1!")

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * int(amount)}'
        bot.send_message(message.chat.id, text)


#5. Запуск бота.
bot.polling(none_stop=True)

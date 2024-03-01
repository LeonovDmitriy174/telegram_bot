import os
import requests
import json
import datetime
import telebot

API_BOT = os.environ.get("TELEGRAM_BOT_API_KEY")
API_APILayer = os.environ.get("APILayer_KEY")


def all_rate():
    """Возвращает список и строку всех валют, доступных к отслеживанию"""
    url = f"https://api.apilayer.com/exchangerates_data/symbols"
    response = requests.get(url, headers={'apikey': API_APILayer})
    response_data = json.loads(response.text)
    rate = response_data['symbols']
    list_rate = []
    for key, value in rate.items():
        list_rate.append(key)
    str_rate = ', '.join(list_rate)
    return str_rate, list_rate


def get_currency_rate(base: str):
    """Возвращает курс введенной валюты"""
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={base}"
    response = requests.get(url, headers={'apikey': API_APILayer})
    response_data = json.loads(response.text)
    rate = response_data['rates']['RUB']
    timestamp = response_data['timestamp']
    return rate, timestamp


def checking_file(rate):
    """Возвращает булевое значение изменился ли курс и содержимое json-file"""
    with open('json-file.json', 'r') as json_file:
        file = json.loads(json_file.read())
        file.sort(key=lambda k: k['timestamp'], reverse=True)
        try:
            rate != file[0]['rate']
        except IndexError:
            return True, file
        except KeyError:
            return True, file
        else:
            if rate == file[0]['rate']:
                return False, file
            else:
                return True, file


def add_to_file(rate, file, timestamp, currency):
    """Добавляет в json-file обновленный курс"""
    file.append({'rate': rate,
                 'timestamp': timestamp,
                 'currency': currency})
    file.sort(key=lambda k: k['timestamp'], reverse=True)
    with open('json-file.json', 'w') as json_file:
        json.dump(file, json_file)


def from_telegram(chat_id, message):
    """Отправляет сообщение с курсом в telegram"""
    url = f"https://api.telegram.org/bot{API_BOT}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()


def time_function(time_interval):
    """Через каждую минуту сравнивает текущий курс и последний записанный.
    При совпадении ничего не происходит,
    при изменении - информация в json-файле обновляется и отправляется умедомление в telegram"""
    datetime_now = datetime.datetime.now()


"""def telebot_start_and_help():
    bot = telebot.TeleBot(API_BOT)
    bot.polling()
    str_rate, list_rate = all_rate()

    @bot.message_handler(commands=['start'])
    def work_start(message):
        bot.send_message(message.chat.id, f'Приветствую!\n'
                                          f'Я бот для отслеживания курса валют.\n'
                                          f'Могу предложить к отслеживанию:\n'
                                          f'{str_rate}')

    @bot.message_handler(commands=['help'])
    def work_help(message):
        bot.send_message(message.chat.id, 'Чем я могу тебе помочь?')

    @bot.message_handler(content_types=['text', 'document', 'audio'])
    def work_command(message):
        user_rate = message.text.upper()
        while user_rate not in list_rate:
            bot.send_message(message.chat.id, 'Пожалуйста, выберите валюту из списка')
        rate = get_currency_rate(user_rate)
        bot.send_message(message.chat.id, f'{rate}\n Желаете получать уведомления при изменении курса?')


def telebot_change_notifications():
    bot = telebot.TeleBot(API_BOT)
    bot.polling()

    @bot.message_handler(content_types=['text', 'document', 'audio'])
    def work_command(message):
        if message.text not in ['yes', 'true', 't', 'y', 'ye', 'да', 'д']:
            bot.send_message(message.chat.id, 'До новых встреч!')
        else:
            pass"""

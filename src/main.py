import os
import requests
import json
import datetime

from functions import (get_currency_rate,
                       checking_file,
                       all_rate,
                       add_to_file,
                       from_telegram)

chat_id = os.environ.get('TELEGRAM_CHAT_ID')

str_rate, list_rate = all_rate()
currency = input(f'Приветствую!\n'
                  f'Я бот для отслеживания курса валют.\n'
                  f'Могу предложить к отслеживанию:\n'
                  f'{str_rate}\n').upper()

while currency not in list_rate:
    currency = input(f'Пожалуйста, выберите валюту из списка\n').upper()

rate, timestamp = get_currency_rate(currency)
print(rate)

bool_check, file = checking_file(rate)

if bool_check:
    add_to_file(rate, file, timestamp, currency)

user_answer = input(f'Желаете получать уведомления в telegram при изменении курса?[yes]\n').lower()

if user_answer not in ['yes', 'true', 't', 'y', 'ye', 'да', 'д', '']:
    exit()

from_telegram(chat_id, rate)


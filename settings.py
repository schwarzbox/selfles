#!/usr/bin/env python3
# IBOT

import os
from urllib.parse import urljoin


NO_DEBUG = os.getenv('NO_DEBUG', False)
if NO_DEBUG is False:
    # pip3 install python-dotenv
    # TOKEN .env
    from dotenv import load_dotenv
    load_dotenv()

# Press "Reveal Config Vars" in settings tab on Heroku and set TOKEN variable
TOKEN = os.getenv('TOKEN', '')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
ADMIN = os.getenv('ADMIN', '')
PROJECT_NAME = os.getenv('PROJECT_NAME', 'selfles')
PORT = os.getenv('PORT', 8000)

DB_URL = os.getenv('DATABASE_URL', '')

WEBHOOK_HOST = f'https://{PROJECT_NAME}.herokuapp.com/'
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)

MESSAGE = 'Alarm!'
NOTIFY = False
HINTS = True
SAVE_DELAY = 16
DELETE_DELAY = 16

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

RHASH = 'https://robohash.org/'
ZEN = 'https://zenquotes.io/api/random/'

GREET = ['Good day', 'Spring coming', 'Keep calm', 'Hello']
EMO = [
    '๐', '๐ฅณ', '๐', '๐คฉ', '๐', '๐', '๐', '๐', '๐', '๐',
    '๐', '๐', '๐', '๐', '๐', '๐', 'โบ๏ธ', '๐', '๐', '๐ฌ',
    '๐คจ', '๐', '๐', '๐', '๐', 'โน๏ธ', '๐', '๐ค', '๐ถ', '๐ด'
]
ICONS = {
    'bot': '๐ค',
    'tools': '๐งฐ',
    'help': '๐ ',
    'date': '๐',
    'note': '๐',
    'sun': 'โ๏ธ',
    'timer': 'โฐ',
    'stop': 'โ๏ธ',
    'map': '๐บ',
    'locate': '๐',
    'gmt': '๐',
    'cancel': 'โ\u200c',
    'set': 'โ๏ธ',
    'quote': '๐',
    'author': '๐ค',
    'add': 'โ',
    'haiku': '๐๏ธ',
    'flower': '๐ฎ',
    'zen': '๐ก',
    'query': '๐',
    'echo': '๐ฃ',
    'hints_on': '๐จ',
    'hints_off': '๐ค',
}

HELP = f"""{ICONS["help"]} Help
/start
/avatar /ava SEED
/date /d DD/MM/YYYY NOTE
/timer /t HH:MM
/stop /s
/boltology /b QUOTE AUTHOR
/haiku /ha SEED
/zen /z
/hints /hi
/help /h
/tool /to
/cancel /c
"""

HINTS_ACTIONS = [
    'set_date', 'set_timer', 'set_boltology', 'set_haiku', 'set_avatar'
]

MENU = {
    'date': [f'{ICONS["date"]} DD/MM/YYYY', f'{ICONS["note"]} NOTE'],
    'timer': [f'{ICONS["timer"]} HH:MM', ''],
    'boltology': [f'{ICONS["quote"]} QUOTE', f'{ICONS["author"]} AUTHOR'],
    'haiku': [f'{ICONS["flower"]} SEED', ''],
    'avatar': [f'{ICONS["bot"]} SEED', '']
}

DONE = 'CAACAgIAAxkBAAIVo2BuF60gZ2X35p7opkiAm7Jgnng8AAJ8BwACRvusBFbHjRbq1BEqHgQ'

STICKERS = {
    'DogLiveBelarus':
    'CAACAgIAAxkBAAIVrGBuGRSD6iIqGSNTdlXho4U9PWPeAAJjAgACVp29CpFl1L2yjiVxHgQ',
    'DogOK':
    'CAACAgIAAxkBAAIV_mBuH0zICrCk5DDoXQndW2VXvogpAALYAANWnb0KiQndv0vxFCceBA',
    'DogQuestion':
    'CAACAgIAAxkBAAIWCGBuH9hQLMPtysXDzVreacU-8tWyAALjAANWnb0KD_gizK2mCzceBA',
    'PlayDog':
    'CAACAgIAAxkBAAIWl2BvSrGgWG9B1cax7VZBZrYvtdyzAALaAANWnb0Kcpw3G94HGzseBA',
    'CryDog':
    'CAACAgIAAxkBAAIWmWBvSuhLpgF01FQ9M7pFvPLf1h7sAAK7AANWnb0KmQ4hyMXo8kgeB',
    'PlaneDog':
    'CAACAgIAAxkBAAIWm2BvSwqu75Lt62tbAheBEQONhAGqAALVAANWnb0K95fBF1yaTuceBA',
    'NoDog':
    'CAACAgIAAxkBAAIWnWBvSys8pvMY57ucC_TQ2qrS-mdbAALJAANWnb0Kfr_SKGk9RyIeBA',
    'StopDog':
    'CAACAgIAAxkBAAIWn2BvS0V9iCnjqIwRcz3sTW-LJgNiAALfAANWnb0KEEh8kSOlJ_0eBA'
}

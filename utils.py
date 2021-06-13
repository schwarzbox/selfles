#!/usr/bin/env python3
# selfles

import datetime
import json
import logging
from random import randint

import pytz
from tzwhere import tzwhere

import crud

from nn.haiku import haiku

import keyboards as kb

import requests

import settings


TZWHERE = tzwhere.tzwhere()


def logging_user(event):
    # event.get_full_command()
    logging.info(event.get_command())
    logging.info(event.from_user)


def get_user(event):
    user_id = event.from_user.id
    crud.create_user(
        user_id,
        datetime.datetime.now().replace(hour=0, minute=0,
                                        second=0, microsecond=0),
        settings.MESSAGE,
        datetime.datetime.now().replace(second=0, microsecond=0),
    )
    user = crud.read_user(user_id)
    return user_id, user


def is_admin(event):
    return (event.from_user.id == settings.ADMIN_ID
            and event.from_user.last_name == settings.ADMIN)


def get_avatar(seed):
    ava_url = f'{settings.RHASH}{seed}'
    response = requests.get(ava_url)
    return response.content


def get_time_zone(location):
    timezone_str = TZWHERE.tzNameAt(
        location['latitude'], location['longitude']
    )
    return pytz.timezone(timezone_str)


def get_notification_message(future_date, message):
    date_fmt = future_date.strftime('%d-%m-%Y')
    now = datetime.datetime.now()
    days = (future_date - now).days
    if days <= 0:
        days = 0
        index = 0
    elif days < len(settings.EMO):
        index = days
    else:
        index = len(settings.EMO) - 1

    return f'{settings.ICONS["date"]} {date_fmt}\n{settings.ICONS["note"]} {message}\n{settings.ICONS["sun"]} {days}\n{settings.EMO[index]}'


def get_random_boltology_message():
    all_quotes = crud.read_all_quotes()
    random_quote = all_quotes[randint(0, len(all_quotes) - 1)]
    return f'{settings.ICONS["quote"]} {random_quote[0]}\n{settings.ICONS["author"]} {random_quote[1]}'


def get_haiku(seed=' '):
    striped = []
    for word in haiku(seed).split('\n')[1:-1]:
        w = word.strip()
        if w:
            striped.append(w)

    result = '\n'.join(striped[:3])
    return f'{settings.ICONS["haiku"]}\n{result}'


def get_zen():
    response = requests.get(settings.ZEN)
    data = json.loads(response.text)[0]
    return f'{settings.ICONS["zen"]} {data["q"]}\n{settings.ICONS["author"]} {data["a"]}'


def switch_keyboard(hints):
    if hints:
        kb.fulltool_kb = kb.fulltool_kb_off
    else:
        kb.fulltool_kb = kb.fulltool_kb_on


def switch_hints(user_id, user, event):
    hints = user[5]

    switch_keyboard(hints)

    hints = not hints

    crud.update_user_hints(user_id, hints)
    return hints, kb.fulltool_kb

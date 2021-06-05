#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IBOT
"""
from random import randint

import datetime

import logging

import asyncio

import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.webhook import get_new_configured_app

import crud

import forms

import keyboards as kb

import settings

import utils


__version__ = 1.0

# ibot.py

# MIT License
# Copyright (c) 2021 Alexander Veledzimovich veledz@gmail.com

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.


# heroku ps:scale web=1 -a ibot-appl
# heroku ps:scale clock=1
# heroku ps:scale worker=0
# logs
# heroku logs --tail -a ibot-appl

# ping GMT
# http: // kaffeine.herokuapp.com

# sheduler (credit card)
# heroku addons:create -a ibot-application scheduler:standard


logging.basicConfig(level=logging.INFO)

TASKS = {}
LOCATION = {}
IBOT = Bot(token=settings.TOKEN)
DISP = Dispatcher(bot=IBOT, storage=MemoryStorage())


async def delete_event(event: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await event.delete()
    logging.info(f'Delete event')


async def restart_notify_task(user_id):
    await cancel_notify_task(user_id)

    TASKS[user_id] = asyncio.create_task(notify_task(user_id))


async def cancel_notify_task(user_id):
    task = TASKS.get(user_id)
    if task and not task.cancelled():
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            TASKS[user_id] = None
            logging.info(f'Cancel notify task: {user_id}')


async def notify_task(user_id):
    while True:
        user = crud.read_user(user_id)
        message = user[2]
        period = user[3]

        ftime = datetime.datetime.strptime(period, settings.DATETIME_FORMAT)
        utc = datetime.datetime.utcnow().replace(microsecond=0)
        sec = (ftime - utc).seconds

        try:
            await asyncio.sleep(sec)
        except asyncio.CancelledError:
            logging.info(f'Cancel notify task: {user_id}')
            raise

        await asyncio.sleep(settings.SAVE_DELAY)

        future_date = datetime.datetime.strptime(
            user[1], settings.DATETIME_FORMAT
        )

        await IBOT.send_message(
            user_id, utils.get_notification_message(future_date, message),
            parse_mode=types.ParseMode.HTML,
            reply_markup=kb.date_kb)

        ftime += datetime.timedelta(days=1)

        if ftime >= future_date:
            await IBOT.send_sticker(user_id, settings.DONE,
                                    disable_notification=True)

            await cancel_notify_task(user_id)

            crud.update_user_period(user_id, period, False)

            logging.info(f'Finish notify task: {user_id}')
            return
        else:
            crud.update_user_period(user_id, ftime, True)


@ DISP.callback_query_handler(lambda cb: True)
async def callback_handler(callback_query: types.CallbackQuery):
    action = callback_query.data
    message = callback_query.message
    message.from_user = callback_query.from_user

    user_id, user = utils.get_user(message)
    hints = user[5]

    if (action in ['set_date', 'set_timer', 'set_boltology',
                   'set_haiku', 'set_avatar']
            and hints):
        key = action.split('_')[1]

        menu = settings.MENU.get(key)
        await IBOT.answer_callback_query(
            callback_query.id,
            f'{settings.ICONS["hints_on"]}\n\nHint!\n\n{menu[0]}\n{menu[1]}',
            show_alert=True
        )
    else:
        await IBOT.answer_callback_query(callback_query.id)

    if action == 'start':
        await start_handler(message)
    elif action == 'set_avatar':
        first = message.from_user.first_name
        last = message.from_user.last_name
        name = ''
        if first and last:
            name = f'{first} {last}'
        elif first:
            name = first
        elif last:
            name = last
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                             one_time_keyboard=True)
        keyboard.add(types.KeyboardButton(name))
        username = message.from_user.username
        if username:
            keyboard.add(types.KeyboardButton(username))
        keyboard.add(kb.cancel)

        await forms.AvatarForm.seed.set()
        await IBOT.send_message(callback_query.from_user.id,
                                f'{settings.ICONS["bot"]}',
                                reply_markup=keyboard)
    elif action == 'date':
        await date_handler(message)
    elif action == 'set_date':
        await forms.DateForm.date.set()
        await IBOT.send_message(callback_query.from_user.id,
                                f'{settings.ICONS["date"]}',
                                reply_markup=kb.cancel_kb)
    elif action == 'timer':
        await timer_handler(message)
    elif action == 'set_timer':
        await forms.TimerForm.period.set()
        await IBOT.send_message(callback_query.from_user.id,
                                f'{settings.ICONS["timer"]}',
                                reply_markup=kb.num_kb)
    elif action == 'stop':
        await stop_handler(message)
    elif action == 'boltology':
        await boltology_handler(message)
    elif action == 'set_boltology':
        await forms.BoltoForm.quote.set()
        await IBOT.send_message(callback_query.from_user.id,
                                f'{settings.ICONS["quote"]}',
                                reply_markup=kb.cancel_kb)
    elif action == 'more_bolto':
        await IBOT.edit_message_text(utils.get_random_boltology_message(),
                                     callback_query.message.chat.id,
                                     callback_query.message.message_id,
                                     reply_markup=kb.more_bolto_kb)
    elif action == 'set_haiku':
        await forms.HaikuForm.seed.set()
        await IBOT.send_message(callback_query.from_user.id,
                                f'{settings.ICONS["flower"]}',
                                reply_markup=kb.haiku_kb)
    elif action == 'more_haiku':
        seed = message.text.split(' ')[1]

        await IBOT.edit_message_text(utils.get_haiku(seed),
                                     callback_query.message.chat.id,
                                     callback_query.message.message_id,
                                     reply_markup=kb.more_haiku_kb)
    elif action == 'zen':
        await zen_handler(message)

    elif action == 'more_zen':
        await IBOT.edit_message_text(utils.get_zen(),
                                     callback_query.message.chat.id,
                                     callback_query.message.message_id,
                                     reply_markup=kb.more_zen_kb)
    elif action == 'hints':
        _, keyboard = utils.switch_hints(user_id, user, message)

        await IBOT.edit_message_text(
            callback_query.message.text,
            callback_query.message.chat.id,
            callback_query.message.message_id,
            reply_markup=keyboard)
    elif action == 'tool':
        await tool_handler(message)
    elif action == 'help':
        await help_handler(message)

# cancel handler


@ DISP.message_handler(commands=['cancel', 'c'], state='*')
@ DISP.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(event: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info(f'Cancel state: {current_state}')

    await state.finish()

    await event.answer(f'{settings.ICONS["cancel"]}\u200c',
                       disable_notification=True,
                       reply_markup=kb.tool_kb)

# handlers


@ DISP.message_handler(commands=['start', 's'])
async def start_handler(event: types.Message):
    utils.logging_user(event)

    starts = settings.GREET[randint(0, len(settings.GREET) - 1)]
    message = f'{settings.ICONS["bot"]} {starts}, {event.from_user.get_mention(as_html=True)}!'

    user_id, user = utils.get_user(event)
    utils.switch_keyboard(not user[5])

    await event.answer(
        message,
        parse_mode=types.ParseMode.HTML,
        reply_markup=kb.fulltool_kb
    )


@ DISP.message_handler(state=forms.AvatarForm.seed)
async def avatar_process(event: types.Message, state: FSMContext):
    event['text'] = f'/ava {event.text}'
    event['entities'] = [
        {'type': 'bot_command', 'offset': 0, 'length': len(event.text)}
    ]
    await avatar_handler(event)
    await state.finish()


@ DISP.message_handler(commands=['avatar', 'ava'])
async def avatar_handler(event: types.Message):
    utils.logging_user(event)
    seed = event.get_args() or ' '

    avatar = utils.get_avatar(seed)

    await IBOT.send_photo(event.from_user.id,  avatar,
                          parse_mode=types.ParseMode.HTML,
                          disable_notification=True,
                          reply_markup=kb.tool_kb)


@ DISP.message_handler(state=forms.DateForm.date)
async def date_process(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = event.text

    await forms.DateForm.next()
    await event.answer(
        f'{settings.ICONS["note"]} NOTE',
        reply_markup=kb.note_kb
    )


@ DISP.message_handler(state=forms.DateForm.note)
async def note_process(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['note'] = event.text

    event['text'] = f'/d {data["date"]} {data["note"]}'
    event['entities'] = [
        {'type': 'bot_command', 'offset': 0, 'length': len(event.text)}
    ]
    await date_handler(event)
    await state.finish()


@ DISP.message_handler(commands=['date', 'd'])
async def date_handler(event: types.Message):
    utils.logging_user(event)

    user_id, user = utils.get_user(event)

    future_date = datetime.datetime.strptime(user[1], settings.DATETIME_FORMAT)

    message = user[2]
    is_notify = user[4]
    args = event.get_args()
    if args:
        date, *new_message = args.split(' ')
        if new_message:
            message = ' '.join(new_message)

        date = date.split('/')
        year, month, day = (future_date.year,
                            future_date.month,
                            future_date.day)

        if len(date) > 2 and all(i.isdigit() for i in date):
            year = int(date[2])
            month = int(date[1])
            day = int(date[0])
        elif len(date) > 1 and all(i.isdigit() for i in date):
            month = int(date[1])
            day = int(date[0])
        elif len(date) > 0 and date[0].isdigit():
            day = int(date[0])
        else:
            await event.answer(
                '/date DD/MM/YYYY NOTE',
                parse_mode=types.ParseMode.HTML,
                reply_markup=kb.rm_kb
            )
            return

        future_date = datetime.datetime(year, month, day, 0, 0, 0)
        crud.update_user_date(user_id, future_date, message)

        if is_notify:
            await restart_notify_task(user_id)
            logging.info(f'Restart notify task: {user_id}')

    await event.answer(
        utils.get_notification_message(future_date, message),
        parse_mode=types.ParseMode.HTML,
        disable_notification=True,
        reply_markup=kb.date_kb
    )


@ DISP.message_handler(state=forms.TimerForm.period)
async def period_process(event: types.Message, state: FSMContext):
    location = LOCATION.get(event.from_user.id)
    if location:
        event['location'] = location
        event['text'] = f'/t {event.text}'
        event['entities'] = [
            {'type': 'bot_command', 'offset': 0, 'length': len(event.text)}
        ]
        await timer_handler(event)
        await state.finish()
    else:
        async with state.proxy() as data:
            data['period'] = event.text

        await forms.TimerForm.next()
        await event.answer(
            f'{settings.ICONS["map"]}',
            disable_notification=True,
            reply_markup=kb.loc_kb
        )


@ DISP.message_handler(content_types=['location'], state=forms.TimerForm.timezone)
async def timezone_process(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event['text'] = f'/t {data["period"]}'
    event['location'] = event.location
    event['entities'] = [
        {'type': 'bot_command', 'offset': 0, 'length': len(event.text)}
    ]

    await timer_handler(event)
    await state.finish()


@ DISP.message_handler(commands=['timer', 't'])
async def timer_handler(event: types.Message):
    utils.logging_user(event)

    user_id, user = utils.get_user(event)

    period = user[3]

    now = event.date.replace(microsecond=0)
    hour, minute, gmt = (None, None, '')

    args = event.get_args()

    if args:
        if args.find(':') > 0:
            hour, minute = args.split(':')

            year, month, day, hours, minutes = (now.year, now.month,
                                                now.day, now.hour,
                                                now.minute)

            if hour.isdigit() and minute and minute.isdigit():
                hours = int(hour)
                minutes = int(minute)
            else:
                await event.answer(
                    '/timer HH:MM',
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=kb.rm_kb
                )
                return

            ftime = datetime.datetime(year, month, day, hours, minutes, 0)

            LOCATION[event.from_user.id] = event.location

            timezone = utils.get_time_zone(event.location)

            if ftime < now:
                ftime += datetime.timedelta(days=1)

            strtime = ftime.strftime('%H:%M %d-%m-%Y')

            ftime -= timezone.utcoffset(now)

            crud.update_user_period(user_id, ftime, True)

            await restart_notify_task(user_id)
            logging.info(f'Create/update notify task: {user_id}')
        else:
            await event.answer(
                '/timer HH:MM',
                parse_mode=types.ParseMode.HTML,
                reply_markup=kb.rm_kb
            )
            return
    else:
        ftime = datetime.datetime.strptime(period, settings.DATETIME_FORMAT)
        location = LOCATION.get(event.from_user.id, event.location)
        if location:
            timezone = utils.get_time_zone(location)
            ftime += timezone.utcoffset(now)
        else:
            gmt = settings.ICONS['gmt']

        strtime = ftime.strftime('%H:%M %d-%m-%Y')

    await event.answer(
        f'{settings.ICONS["timer"]} {strtime} {gmt}',
        parse_mode=types.ParseMode.HTML,
        disable_notification=True,
        reply_markup=kb.timer_kb
    )


@ DISP.message_handler(commands=['stop'])
async def stop_handler(event: types.Message):
    utils.logging_user(event)

    user_id, user = utils.get_user(event)

    await cancel_notify_task(user_id)

    period = user[3]
    crud.update_user_period(user_id, period, False)

    logging.info(f'Stop notify task: {user_id}')

    await event.answer(
        f'{settings.ICONS["timer"]} {settings.ICONS["stop"]}',
        parse_mode=types.ParseMode.HTML,
        disable_notification=True,
        reply_markup=kb.tool_kb
    )


@ DISP.message_handler(state=forms.BoltoForm.quote)
async def quote_process(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quote'] = event.text

    await forms.BoltoForm.next()
    await event.answer(
        f'{settings.ICONS["author"]} AUTHOR',
        reply_markup=kb.cancel_kb
    )


@ DISP.message_handler(state=forms.BoltoForm.author)
async def author_process(event: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['author'] = event.text

    crud.create_quote(data["quote"], data["author"])

    event['text'] = f'/b {settings.ICONS["quote"]} {data["quote"]}\n{settings.ICONS["author"]} {data["author"]}'
    event['entities'] = [
        {'type': 'bot_command', 'offset': 0, 'length': len(event.text)}
    ]
    await boltology_handler(event)
    await state.finish()


@ DISP.message_handler(commands=['boltology', 'b'])
async def boltology_handler(event: types.Message):
    utils.logging_user(event)

    args = event.get_args()

    if args:
        await event.answer(
            args,
            parse_mode=types.ParseMode.HTML,
            disable_notification=True,
            reply_markup=kb.rm_kb
        )
    else:
        await event.answer(
            utils.get_random_boltology_message(),
            parse_mode=types.ParseMode.HTML,
            disable_notification=True,
            reply_markup=kb.more_bolto_kb
        )


@ DISP.message_handler(state=forms.HaikuForm.seed)
async def haiku_process(event: types.Message, state: FSMContext):
    event['text'] = f'/ha {event.text}'
    event['entities'] = [
        {'type': 'bot_command', 'offset': 0, 'length': len(event.text)}
    ]
    await haiku_handler(event)
    await state.finish()


@ DISP.message_handler(commands=['haiku', 'ha'])
async def haiku_handler(event: types.Message):
    utils.logging_user(event)

    generate = utils.get_haiku(event.get_args())

    await event.answer(generate,
                       parse_mode=types.ParseMode.HTML,
                       disable_notification=True,
                       reply_markup=kb.more_haiku_kb)


@ DISP.message_handler(commands=['zen', 'z'])
async def zen_handler(event: types.Message):
    utils.logging_user(event)

    await event.answer(
        utils.get_zen(),
        parse_mode=types.ParseMode.HTML,
        disable_notification=True,
        reply_markup=kb.more_zen_kb
    )


@ DISP.message_handler(commands=['help', 'h'])
async def help_handler(event: types.Message):
    utils.logging_user(event)

    help_cmd = settings.HELP
    if utils.is_admin(event):
        help_cmd = f'{settings.HELP}\n/database /db'
    await event.answer(
        help_cmd,
        parse_mode=types.ParseMode.HTML,
        reply_markup=kb.tool_kb
    )


@ DISP.message_handler(commands=['tool', 'to'])
async def tool_handler(event: types.Message):
    utils.logging_user(event)

    user_id, user = utils.get_user(event)
    utils.switch_keyboard(not user[5])

    await event.answer(
        f'{settings.ICONS["tools"]} Tools',
        parse_mode=types.ParseMode.HTML,
        reply_markup=kb.fulltool_kb
    )


@ DISP.message_handler(commands=['hints', 'hi'])
async def hints_handler(event: types.Message):
    utils.logging_user(event)

    user_id, user = utils.get_user(event)

    hints, _ = utils.switch_hints(user_id, user, event)
    text = settings.ICONS['hints_off']
    if hints:
        text = settings.ICONS['hints_on']

    await event.answer(f'{text}\u200c',
                       disable_notification=True,
                       reply_markup=kb.tool_kb)


@ DISP.message_handler(commands=['database', 'db'])
async def database_handler(event: types.Message):
    utils.logging_user(event)

    if utils.is_admin(event):
        logging.info('TASKS')
        logging.info(TASKS)
        logging.info('LOCATION')
        logging.info(LOCATION)

        me = await IBOT.get_me()
        await event.answer(
            f'Users: {crud.read_all_users()}\n\nMe: {me}',
            parse_mode=types.ParseMode.HTML,
            disable_notification=True,
            reply_markup=kb.help_kb
        )


@ DISP.message_handler()
async def echo_handler(event: types.Message):
    utils.logging_user(event)
    # import aiogram.utils.markdown as md
    # md.text(md.code(event.get_args() or '\U0001F31A')

    await event.answer(
        f'{settings.ICONS["echo"]} {event.text}',
        parse_mode=types.ParseMode.MARKDOWN,
        disable_notification=True,
        reply_markup=kb.tool_kb
    )


@ DISP.message_handler(content_types=types.ContentType.ANY)
async def any_message(event: types.Message):
    utils.logging_user(event)

    dogs = list(settings.STICKERS.values())
    index = randint(0, len(dogs) - 1)

    await IBOT.send_sticker(event.from_user.id,
                            sticker=dogs[index],
                            reply_markup=kb.tool_kb)

    # await delete_event(event, settings.DELETE_DELAY)
    # await delete_event(ev, settings.DELETE_DELAY)


async def on_load():
    users = crud.read_all_users()

    for user in users:
        user_id = user[0]
        is_notify = user[4]

        if is_notify:
            await restart_notify_task(user_id)
            logging.info(f'Restart notify task: {user_id}')


async def on_debug():
    await on_load()

    try:
        await DISP.start_polling()
    finally:
        await IBOT.close()


async def on_startup(app):
    await on_load()

    await IBOT.delete_webhook()
    await IBOT.set_webhook(settings.WEBHOOK_URL)


if __name__ == '__main__':
    if settings.NO_DEBUG:
        app = get_new_configured_app(
            dispatcher=DISP, path=settings.WEBHOOK_URL_PATH
        )
        app.on_startup.append(on_startup)
        aiohttp.web.run_app(app, host='0.0.0.0', port=settings.PORT)

    else:
        asyncio.run(on_debug())

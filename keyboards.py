#!/usr/bin/env python3
# SELFLES

from aiogram.types import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import settings

force_kb = ForceReply()

rm_kb = ReplyKeyboardRemove()

cancel = KeyboardButton(settings.ICONS['cancel'])
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_kb.add(cancel)

location = KeyboardButton(settings.ICONS['locate'], request_location=True)
loc_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
loc_kb.add(location)
loc_kb.add(cancel)

midnight = KeyboardButton('00:00')
eight = KeyboardButton('08:00')
ten = KeyboardButton('10:00')
fourteen = KeyboardButton('14:00')
sixteen = KeyboardButton('16:00')
twenty = KeyboardButton('20:00')

num_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
num_kb.add(midnight, eight, ten)
num_kb.add(sixteen, fourteen, twenty)
num_kb.add(cancel)

alarm = KeyboardButton('Alarm!')
roll = KeyboardButton('Let\'s roll!')
note_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
note_kb.add(alarm, roll)
note_kb.add(cancel)

spring = KeyboardButton('Весна')
silence = KeyboardButton('Тишина')
temple = KeyboardButton('Храм')
haiku_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
haiku_kb.add(spring, silence, temple)
haiku_kb.add(cancel)

bstart = InlineKeyboardButton('Start', callback_data='start')

bavatar = InlineKeyboardButton(settings.ICONS['bot'],
                               callback_data='set_avatar')
bdate = InlineKeyboardButton(settings.ICONS['date'],
                             callback_data='date')
bset_date = InlineKeyboardButton(settings.ICONS['set'],
                                 callback_data='set_date')
btimer = InlineKeyboardButton(settings.ICONS['timer'],
                              callback_data='timer')
bset_timer = InlineKeyboardButton(settings.ICONS['set'],
                                  callback_data='set_timer')
bstop = InlineKeyboardButton(settings.ICONS['stop'],
                             callback_data='stop')
bbolt = InlineKeyboardButton(settings.ICONS['quote'],
                             callback_data='boltology')
bset_bolt = InlineKeyboardButton(settings.ICONS['add'],
                                 callback_data='set_boltology')
bmore_bolto = InlineKeyboardButton(settings.ICONS['quote'],
                                   callback_data='more_bolto')

bset_haiku = InlineKeyboardButton(settings.ICONS['haiku'],
                                  callback_data='set_haiku')
bmore_haiku = InlineKeyboardButton(settings.ICONS['haiku'],
                                   callback_data='more_haiku')
bzen = InlineKeyboardButton(settings.ICONS['zen'],
                            callback_data='zen')
bmore_zen = InlineKeyboardButton(settings.ICONS['zen'],
                                 callback_data='more_zen')
btool = InlineKeyboardButton(settings.ICONS['tools'],
                             callback_data='tool')
bhelp = InlineKeyboardButton(settings.ICONS['help'],
                             callback_data='help')
bhints_on = InlineKeyboardButton(settings.ICONS['hints_on'],
                                 callback_data='hints')
bhints_off = InlineKeyboardButton(settings.ICONS['hints_off'],
                                  callback_data='hints')

bquery = InlineKeyboardButton(settings.ICONS['query'],
                              switch_inline_query='🤍❤️🤍')
# bquery_curent = InlineKeyboardButton(
#     'Draft', switch_inline_query_current_chat='I am iBot'
# )

more_bolto_kb = InlineKeyboardMarkup().add(bmore_bolto, btool)
more_haiku_kb = InlineKeyboardMarkup().add(bmore_haiku, btool)
more_zen_kb = InlineKeyboardMarkup().add(bmore_zen, btool)


date_kb = InlineKeyboardMarkup().add(bset_date, btool)
timer_kb = InlineKeyboardMarkup().add(bstop, bset_timer, btool)
tool_kb = InlineKeyboardMarkup().add(btool)
help_kb = InlineKeyboardMarkup().add(bhelp, btool)

fulltool_kb_on = InlineKeyboardMarkup(row_width=3)
fulltool_kb_on.add(bavatar)
fulltool_kb_on.row(bdate, bset_date)
fulltool_kb_on.add(btimer, bset_timer)
fulltool_kb_on.add(bbolt, bset_bolt)
fulltool_kb_on.add(bset_haiku)
fulltool_kb_on.add(bzen)
fulltool_kb_on.add(bhints_on, bquery)
fulltool_kb_on.add(bhelp)

fulltool_kb_off = InlineKeyboardMarkup(row_width=3)
fulltool_kb_off.add(bavatar)
fulltool_kb_off.row(bdate, bset_date)
fulltool_kb_off.add(btimer, bset_timer)
fulltool_kb_off.add(bbolt, bset_bolt)
fulltool_kb_off.add(bset_haiku)
fulltool_kb_off.add(bzen)
fulltool_kb_off.add(bhints_off, bquery)
fulltool_kb_off.add(bhelp)

fulltool_kb = fulltool_kb_on

#!/usr/bin/env python3
# IBOT

from aiogram.dispatcher.filters.state import State, StatesGroup


class AvatarForm(StatesGroup):
    seed = State()


class DateForm(StatesGroup):
    date = State()
    note = State()


class TimerForm(StatesGroup):
    period = State()
    timezone = State()


class BoltoForm(StatesGroup):
    quote = State()
    author = State()


class HaikuForm(StatesGroup):
    seed = State()

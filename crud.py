#!/usr/bin/env python3
# SELFLES

import logging
import sqlite3

import settings

logging.basicConfig(level=logging.INFO)

DB = 'bot.db'


def add_user_table():
    conn = sqlite3.connect(DB)
    # conn.execute('DROP TABLE user_db')
    conn.execute(
        'CREATE TABLE user_db (ID INTEGER PRIMARY KEY, FUTUREDATE TIMESTAMP NOT NULL, MESSAGE STRING NOT NULL, PERIOD TIMESTAMP NOT NULL, NOTIFY INTEGER NOT NULL, HINTS INTEGER DEFAULT 1);')
    conn.commit()
    conn.close()


def add_user_field(column):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f'ALTER TABLE user_db ADD COLUMN {column}')
    logging.info(f'Create field: {column}')
    conn.commit()
    conn.close()


def create_user(
    ID,
    date,
    message,
    period,
    notify=settings.NOTIFY,
    hints=settings.HINTS,
):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    exist = cur.execute("SELECT ID FROM user_db WHERE ID = :ID", (ID,))
    if exist.fetchone() is None:
        params = (ID, date, message, period, notify, hints)
        cur.execute('INSERT INTO user_db VALUES (?,?,?,?,?,?)', params)
        conn.commit()
        logging.info(f'Create user: {ID}')
    else:
        logging.info(f'Exist user: {ID}')
    conn.close()


def read_all_users():
    logging.info(f'Read all users')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_db")
    all_users = cur.fetchall()
    conn.close()
    logging.info('Done')
    return all_users


def read_user(ID):
    logging.info(f'Read user: {ID}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_db WHERE ID =:ID', {'ID': ID})
    user = cur.fetchone()

    conn.close()
    logging.info('Done')
    return user


def update_user_date(ID, date, message):
    logging.info(f'Update user: {ID}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('UPDATE user_db SET FUTUREDATE = :FUTUREDATE, MESSAGE = :MESSAGE WHERE ID =:ID ', {
                'FUTUREDATE': date, 'MESSAGE': message, 'ID': ID})
    conn.commit()
    conn.close()
    logging.info('Done')


def update_user_period(ID, period, is_notify):
    logging.info(f'Update user: {ID}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('UPDATE user_db SET PERIOD = :PERIOD, NOTIFY = :NOTIFY WHERE ID =:ID', {
                'PERIOD': period, 'NOTIFY': is_notify, 'ID': ID})
    conn.commit()
    conn.close()
    logging.info('Done')


def update_user_hints(ID, hints):
    logging.info(f'Update user: {ID}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('UPDATE user_db SET HINTS = :HINTS WHERE ID =:ID',
                {'HINTS': hints, 'ID': ID})
    conn.commit()
    conn.close()
    logging.info('Done')


def update_user(ID, date, message, period, is_notify=0, hints=1):
    update_user_date(ID, date, message)
    update_user_period(ID, period, is_notify)
    update_user_hints(ID, hints)


def delete_user(ID):
    logging.info(f'Delete user: {ID}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('DELETE FROM user_db WHERE ID =:ID ', {'ID': ID})

    conn.commit()
    conn.close()
    logging.info('Done')


# quote
def add_quote_table():
    conn = sqlite3.connect(DB)
    conn.execute(
        'CREATE TABLE quote_db (ID INTEGER PRIMARY KEY AUTOINCREMENT, QUOTE STRING NOT NULL, AUTHOR STRING NOT NULL);')
    conn.commit()
    conn.close()


def create_quote(quote, author):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    exist = cur.execute(
        'SELECT QUOTE FROM quote_db WHERE QUOTE = :QUOTE', (quote,)
    )
    if exist.fetchone() is None:
        params = (None, quote, author)
        cur.execute('INSERT INTO quote_db VALUES (?,?,?)', params)
        conn.commit()
        logging.info(f'Create quote: {quote}')
    else:
        logging.info(f'Exist quote: {quote}')
    conn.close()


def read_all_quotes():
    logging.info(f'Read all quotes')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT QUOTE, AUTHOR FROM quote_db')
    all_quotes = cur.fetchall()
    conn.close()
    logging.info('Done')
    return all_quotes


def read_quote(quote):
    logging.info(f'Read quote: {quote}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(
        'SELECT QUOTE, AUTHOR FROM quote_db WHERE QUOTE = :QUOTE', (quote,)
    )
    quote = cur.fetchone()
    conn.close()
    logging.info('Done')
    return quote


def update_quote(quote, author):
    logging.info(f'Update quote: {quote}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    quote_exists = cur.execute(
        'SELECT ID FROM quote_db WHERE QUOTE = :QUOTE', (quote,)
    ).fetchone()
    if quote_exists:
        cur.execute(
            'UPDATE quote_db SET QUOTE = :QUOTE, AUTHOR = :AUTHOR WHERE QUOTE =:QUOTE ', {'QUOTE': quote, 'AUTHOR': author, 'ID': quote_exists[0]})
        conn.commit()
    conn.close()
    logging.info('Done')


def delete_quote(quote):
    logging.info(f'Delete quote: {quote}')
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('DELETE FROM quote_db WHERE QUOTE =:QUOTE ', {'QUOTE': quote})
    conn.commit()
    conn.close()
    logging.info('Done')

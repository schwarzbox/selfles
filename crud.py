#!/usr/bin/env python3
# SELFLES

import logging
import psycopg2
from contextlib import closing

import settings

logging.basicConfig(level=logging.INFO)


def add_user_table():
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        print(db_version)

        cursor.execute(
            """
                CREATE TABLE users (
                    ID INTEGER PRIMARY KEY,
                    FUTUREDATE TIMESTAMP NOT NULL,
                    MESSAGE VARCHAR(1024) NOT NULL,
                    PERIOD TIMESTAMP NOT NULL,
                    NOTIFY BOOL DEFAULT FALSE,
                    HINTS BOOL DEFAULT True
                );
            """
        )
        conn.commit()


def drop_user_table():
    logging.info(f'Drop user table')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute('DROP TABLE users;')

        conn.commit()
        logging.info('Done')


def add_user_field(column, type):
    logging.info(f'Create field: {column}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f'ALTER TABLE users ADD COLUMN {column} {type};'
        )

        conn.commit()
        logging.info('Done')


def create_user(
    ID,
    futuredate,
    message,
    period,
    notify=settings.NOTIFY,
    hints=settings.HINTS
):
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(f'SELECT id FROM users WHERE id = {ID};')
        if cursor.fetchone() is None:
            params = (ID, futuredate, message, period, notify, hints)
            cursor.execute(
                f'INSERT INTO users(ID, futuredate, message, period, notify, hints) VALUES (%s, %s, %s, %s, %s, %s);',
                params
            )
            conn.commit()
            logging.info(f'Create user: {ID}')
        else:
            logging.info(f'Exist user: {ID}')


def read_all_users():
    logging.info(f'Read all users')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users;')
        all_users = cursor.fetchall()

        logging.info('Done')
        return all_users


def read_user(ID):
    logging.info(f'Read user: {ID}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM users WHERE ID = {ID};')
        user = cursor.fetchone()

        logging.info('Done')
        return user


def update_user_date(ID, futuredate, message):
    logging.info(f'Update user: {ID}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f'UPDATE users SET FUTUREDATE = %s, MESSAGE = %s WHERE ID = %s;', (futuredate, message, ID)
        )
        conn.commit()

        logging.info('Done')


def update_user_period(ID, period, is_notify):
    logging.info(f'Update user: {ID}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f'UPDATE users SET PERIOD = %s, NOTIFY = %s WHERE ID = %s;', (period, is_notify, ID)
        )
        conn.commit()

        logging.info('Done')


def update_user_hints(ID, hints):
    logging.info(f'Update user: {ID}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f'UPDATE users SET HINTS = %s WHERE ID = %s;', (hints, ID)
        )
        conn.commit()

        logging.info('Done')


def update_user(
    ID,
    futuredate,
    message,
    period,
    notify=settings.NOTIFY,
    hints=settings.HINTS
):
    update_user_date(ID, futuredate, message)
    update_user_period(ID, period, is_notify)
    update_user_hints(ID, hints)


def delete_user(ID):
    logging.info(f'Delete user: {ID}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(f'DELETE FROM users WHERE id = {ID};')
        conn.commit()

        logging.info('Done')

# quote


def add_quote_table():
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        print(db_version)

        cursor.execute(
            """
                CREATE TABLE quotes (
                    ID SERIAL PRIMARY KEY,
                    QUOTE VARCHAR(1024) NOT NULL,
                    AUTHOR VARCHAR(256) NOT NULL
                );
            """
        )
        conn.commit()


def create_quote(quote, author):
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            'SELECT QUOTE FROM quotes WHERE QUOTE = %s;', (quote,)
        )
        if cursor.fetchone() is None:
            params = (quote, author)
            cursor.execute(
                'INSERT INTO quotes(quote, author) VALUES (%s,%s);', params
            )
            conn.commit()
            logging.info(f'Create quote: {quote}')
        else:
            logging.info(f'Exist quote: {quote}')


def read_all_quotes():
    logging.info(f'Read all quotes')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT QUOTE, AUTHOR FROM quotes;')
        all_quotes = cursor.fetchall()

        logging.info('Done')
        return all_quotes


def read_quote(quote):
    logging.info(f'Read quote: {quote}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            'SELECT QUOTE, AUTHOR FROM quotes WHERE QUOTE = %s;',
            (quote,)
        )
        quote = cursor.fetchone()
        logging.info('Done')
        return quote


def update_quote(quote, author):
    logging.info(f'Update quote: {quote}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            'SELECT QUOTE FROM quotes WHERE QUOTE = %s;', (quote,)
        )
        if cursor.fetchone() is None:
            cur.execute(
                'UPDATE quotes SET QUOTE = %s, AUTHOR = %s WHERE QUOTE = %s;', (quote, author, quote))
            conn.commit()

        logging.info('Done')


def delete_quote(quote):
    logging.info(f'Delete quote: {quote}')
    with closing(psycopg2.connect(settings.DB_URL)) as conn:
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM quotes WHERE QUOTE = %s;', (quote,)
        )
        conn.commit()

        logging.info('Done')

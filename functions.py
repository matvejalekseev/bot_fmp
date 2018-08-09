import random
import re
import sqlite3

from telebot import types

from conf import db


def markup_callbackdata(data):
    markup = types.InlineKeyboardMarkup()
    rowInlne = []
    k = 0
    for row in data:
        k = k + 1
        rowInlne.append(types.InlineKeyboardButton(text=row[0], callback_data="status-" + row[1]))
        if k == 2:
            markup.row(*rowInlne)
            k = 0
            rowInlne = []
    if rowInlne:
        markup.row(*rowInlne)
    return markup


def inchats(s):
    chats = select("select chat_id from chats where chat_id = " + str(s) + ";")
    if chats:
        return True
    else:
        return False

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def prettyUsername(n,un):
    if un != 'None' and un:
        user = "[" + n + "](https://t.me/" + un + ")"
    else:
        user = n
    return user

def prettyUsername_wA(un):
    if un != 'None' and un:
        user = "@" + un
    else:
        user = ''
    return user

def xstr(s):
    if s is None or s == 'None':
        return ''
    else:
        return str(s)

def is_str(s):
    if s is None or s == 'None':
        return False
    else:
        return True

def is_time(s):
    result = re.findall(r'[0,1,2]\d{1}[:][0,1,2,3,4,5]\d{1}', s)
    if len(result) > 0:
        return True
    else:
        return False

def is_phone(s):
    result = re.findall(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', s)
    if len(result) > 0:
        return True
    else:
        return False

def hello(name):
    phrase = ['Привет, ', 'Добрый день, ', 'Здравствуйте, ', 'Аллоха, ']
    i = random.randint(0, 3)
    result = phrase[i] + name + "!\n\n"
    return result

def select(req, db_in = db):
    try:
        conn = sqlite3.connect(db_in)
        cursor = conn.cursor()
        cursor.execute(req)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except:
        pass


def change(req, db_in=db):
    try:
        conn = sqlite3.connect(db_in)
        cursor = conn.cursor()
        cursor.execute(req)
        conn.commit()
        conn.close()
        return True
    except:
        pass


def event(name=None,
          price=None,
          account=None,
          users=None):
    event_name = "*" + xstr(name) + "*\n"
    event_date = "*Сумма:* " + xstr(price) + "\n"
    event_time = "*Перевести:*\n" + xstr(account) + "\n"
    if not(users):
        event_user = "Нет виновника\n"
    else:
        event_user = "*Виновник:*\n"
        for user in users:
            event_user = event_user + prettyUsername(user[0], user[1]) + "\n"
    order = event_name + event_date + event_time + event_user
    return order

def check_event(name, price, account):
    if is_str(name) and is_str(price) and is_str(account):
        return True
    else:
        return False
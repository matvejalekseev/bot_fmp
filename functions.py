import random
import re
import sqlite3
from datetime import datetime
from telebot import types
from conf import db
from msg import *

def admin_list():
    return select("select chat_id from chats where status = 1;")

def user_list():
    return select("select chat_id from chats where status = 0;")

def current_date():
    try:
        day = datetime.now().day
        month = datetime.now().month
        if month < 10:
            current_month = '0' + str(month)
        else:
            current_month = str(month)
        if day < 10:
            current_day = '0' + str(day)
        else:
            current_day = str(day)
        return current_day + '.' + current_month
    except:
        return error

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

def inadminchats(s):
    chats = select("select chat_id from chats where status = 1 and chat_id = " + str(s) + ";")
    if chats:
        return True
    else:
        return False

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
    except:
        return False

def prettyUsername(n,un):
    try:
        if is_str(un):
            user = "[" + n + "](https://t.me/" + xstr(un) + ")"
        else:
            user = n
        return user
    except:
        return error

def prettyUsername_wA(un):
    try:
        if is_str(un):
            user = "@" +xstr(un)
        else:
            user = ''
        return user
    except:
        return error

def xstr(s):
    if s is None or s == 'None':
        return ''
    else:
        return str(s)

def is_str(s):
    if s is None or s == 'None' or s == '':
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
    try:
        phrase = ['Привет, ', 'Добрый день, ', 'Здравствуйте, ', 'Аллоха, ']
        i = random.randint(0, 3)
        result = phrase[i] + name + "!\n\n"
        return result
    except:
        return error
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


def event():
    try:
        row = select("select name, price, account, id, rowid from events where status = 0 "
                     "order by rowid desc limit 1;")
        users_in = select("select name, username from chats where chat_id in "
                           "( select chat_id from u2e where event_id = " + str(row[0][3]) + ");")
        event_name = "*" + xstr(row[0][0]) + "*\n"
        event_date = "*Сумма:* " + xstr(row[0][1]) + "\n"
        event_time = "*Перевести по телефону(Альфа/Сбер):*\n\n```" + xstr(row[0][2]) + "```\n\n"
        if not(users_in):
            event_user = "Нет виновника\n"
        else:
            event_user = "*Виновник:*\n"
            for user in users_in:
                event_user = event_user + prettyUsername(user[0], user[1]) + "\n"
        order = event_name + event_date + event_time + event_user
        return order
    except:
        return error

def check_event():
    row = select("select name, price, account, id, rowid from events where status = 0 "
                 "order by rowid desc limit 1;")
    if is_str(row[0][0]) and is_str(row[0][1]) and is_str(row[0][2]):
        return True
    else:
        return False

def birthday_list():
    try:
        list = select("select birthday,name,username,substr(birthday,1,2) as first from chats where status = 0 "
                      "and substr(birthday,4,2) = '" + current_date()[3:] + "' order by first;")
        if list:
            text = db_label
            for bd in list:
                text = text + bd[0][:2] + " - " + prettyUsername(bd[1], bd[2]) + "\n"
        else:
            text = empty_list_bd
        return text
    except:
        return error


def users_list():
    try:
        list = select("select birthday,name,username,chat_id,substr(birthday,4,2) as first "
                      "from chats where status = 0 order by first;")
        if list:
            text = ladel_users
            for user in list:
                text = text + user[0] + " " + user[1] + " " + prettyUsername_wA(user[2]) + " "\
                       + str(round(user[3])) + "\n"
        else:
            text = empty_list_user
        return text
    except:
        return error

def prettyPrintName(ln, fn):
    try:
        if is_str(ln) and is_str(fn):
            return ln + " " + fn
        if not is_str(ln):
            return fn
        else:
            return fn
    except:
        return error
import re
import random
import sqlite3
from conf import db

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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
    result = phrase[i] + name + "!"
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

def change(req, db_in = db):
    try:
        conn = sqlite3.connect(db_in)
        cursor = conn.cursor()
        cursor.execute(req)
        conn.commit()
        conn.close()
        return True
    except:
        pass

def event(name = None,
          price = None,
          account = None,
          status = None,
          users = None):
    event_name = "*" + xstr(name) + "*\n"
    event_date = "*Сумма:* " + xstr(price) + "\n"
    event_time = "*Перевести:* " + xstr(account) + "\n"
    for user in users:
        event_user = event_user + xstr(user) + "\n"
    event_status = "\n*Статус:* " + xstr(status) + "\n"
    order = event_name + event_date + event_time + event_user + event_status
    return order

def check_event(name, price, account):
    if is_str(name) and is_str(price) and is_str(account):
        return True
    else:
        return False
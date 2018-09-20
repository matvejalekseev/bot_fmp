import random
import re
import sqlite3
from datetime import datetime
from conf import db
from msg import *
from markups import *

def admin_list():
    return select("select chat_id from chats where status = 1;")

def user_list():
    return select("select chat_id from chats where status = 0;")

def user_list_with_name():
    return select("select chat_id,name from chats where status = 0;")

def user_list_to_send():
    return select("select c.chat_id from chats c "
                  "join status_sbor ss on ss.chat_id = c.chat_id and ss.status not in (4) where c.status = 0;")

def user_list_to_send_with_name():
    return select("select c.chat_id,c.name from chats c "
                  "join status_sbor ss on ss.chat_id = c.chat_id and ss.status not in (4) where c.status = 0;")

def update_stop_holiday_date(id, stop_date):
    start_date = select("select date from holidays where chat_id = " + str(id) + ";")[0][0]
    if datetime.strptime(start_date, "%d.%m.%Y") > datetime.strptime(stop_date, "%d.%m.%Y"):
        change("update holidays set date = '" + stop_date + "' where action = 'start' and chat_id = " + str(id) + ";")
        change("insert into holidays(chat_id,date,action) values (" + str(id) + ", '"
               + start_date + "','stop');")
    else:
        change("insert into holidays(chat_id,date,action) values (" + str(id) + ", '"
               + stop_date + "','stop');")

def change_stats(n,s):
    if n > 0:
        change("update stats set number = number+" + str(n) + " where stat = '" + str(s) + "';")
    return True

def change_stats_down(n,s):
    if n > 0:
        change("update stats set number = number-" + str(n) + " where stat = '" + str(s) + "';")
    return True

def current_date():
    try:
        return str(datetime.now().strftime("%d.%m"))
    except:
        return error

def current_date_with_year():
    try:
        return str(datetime.now().strftime("%d.%m.%Y"))
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

def inholiday(s):
    chats = select("select chat_id from status_sbor where status = 4 and chat_id = " + str(s) + ";")
    if chats:
        return True
    else:
        return False

def holidayexists(s):
    chats = select("select chat_id from holidays where chat_id = " + str(s) + ";")
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

def all_event_end():
    if select("select 1 from events where status = 1;"):
        return False
    else:
        return True

def is_open_event(id):
    if select("select 1 from events where status = 1 and id = " + str(id) + ";"):
        return True
    else:
        return False

def is_proccess__user_event(id):
    if select("select status from status_sbor where status = 0 and chat_id = " + str(id) + ";"):
        return True
    else:
        return False

def list_users_to_remind():
      return select("select chat_id from status_sbor where status = 0;")

def event_status():
    try:
        if all_event_end():
            return 'Сбор завершён\n'
        else:
            return 'Сбор открыт\n'
    except:
        return error

def statusName(id):
    try:
        if select("select name from statuses where id = " + str(id) + ";"):
            return select("select name from statuses where id = " + str(id) + ";")[0][0]
        else:
            return "Другое"
    except:
        return error

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

def event_in_proccess():
    try:
        row = select("select name, price, account, id, rowid from events where status = 1 "
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

def holiday_list():
    try:
        in_holiday = select("select c.name,c.username,h.date,substr(h.date,1,2),substr(h.date,4,2),substr(h.date,7,4)"
                            " from chats c join status_sbor ss on ss.chat_id = c.chat_id"
                            " and ss.status = 4 left join holidays h on h.chat_id = c.chat_id and h.action = 'stop' "
                            "where c.status = 0 order by 6,5,4;")
        future_holiday = select("select c.name,c.username,begin.date,end.date,substr(begin.date,1,2),"
                                "substr(begin.date,4,2),substr(begin.date,7,4) from chats c join holidays begin "
                                "on begin.chat_id = c.chat_id and begin.action = 'start' join holidays end "
                                "on end.chat_id = c.chat_id and end.action = 'stop' join status_sbor ss "
                                "on ss.chat_id = c.chat_id and ss.status <> 4 order by 6,5,4;")
        if in_holiday and future_holiday:
            text = in_holiday_label
            for holiday in in_holiday:
                text = text + "До " + holiday[2] + " - " + prettyUsername(holiday[0], holiday[1]) + "\n"
            text = text + "\n" + future_holiday_label
            for holiday in future_holiday:
                text = text + "С " + holiday[2] + " по " + holiday[3] + " - " + prettyUsername(holiday[0], holiday[1]) \
                       + "\n"
        elif future_holiday:
            text = future_holiday_label
            for holiday in future_holiday:
                text = text + "С " + holiday[2] + " по " + holiday[3] + " - " + prettyUsername(holiday[0], holiday[1]) \
                       + "\n"
        elif in_holiday:
            text = in_holiday_label
            for holiday in in_holiday:
                text = text + holiday[2] + " - " + prettyUsername(holiday[0], holiday[1]) + "\n"
        else:
            text = empty_list_holiday
        return text
    except:
        return error


def users_list():
    try:
        list = select("select birthday,name,username,chat_id,substr(birthday,4,2) as first,substr(birthday,1,2) as s "
                      "from chats where status = 0 order by first,s;")
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
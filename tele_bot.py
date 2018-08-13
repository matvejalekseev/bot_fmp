# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import logging
import subprocess
import time
import telebot
from conf import *
from functions import *
from markups import *
from msg import *
from telegramcalendar import create_calendar

logging.basicConfig(filename="logs/tele_bot.log", level=logging.INFO)

current_shown_dates={}

ineventname = []
ineventaccount =[]
ineventprice = []
ineventuser = []

bot = telebot.TeleBot(telegrambot_test)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        str_user = message.text[7:]
        str_current = select("select str from invite limit 1;")[0][0]
        if message.chat.type == 'private':
            if str_user == str_current:
                change("insert into chats(chat_id, username, name) values (" + str(message.chat.id) + ",'"
                   + str(message.chat.username) + "','" +
                   prettyPrintName(message.chat.last_name, message.chat.first_name) + "');")
                change("insert into status_sbor(chat_id) values (" + str(message.chat.id) + ");")
                now = datetime.now()
                chat_id = message.chat.id
                date = (now.year, now.month)
                current_shown_dates[chat_id] = date
                markup = create_calendar(now.year, now.month)
                bot.send_message(message.chat.id, start_msg, reply_markup=markup)
                user_text = prettyUsername(prettyPrintName(message.chat.last_name, message.chat.first_name),
                                           str(message.chat.username))
                for chat in admin_list():
                    bot.send_message(chat[0], msg_new_user + user_text,
                                     parse_mode='MARKDOWN', disable_web_page_preview=True)
            else:
                bot.send_message(message.chat.id, no_invite)
        else:
            bot.send_message(message.chat.id, not_private_msg)
    except:
        pass

@bot.message_handler(commands=['refresh'])
def send_welcome(message):
    try:
        if message.chat.type == 'private':
            if inchats(message.chat.id):
                change("update chats set username ='" + str(message.chat.username) + "', name ='" +
                       prettyPrintName(message.chat.last_name, message.chat.first_name)
                       + "' where chat_id = " + str(message.chat.id) + ";")
                now = datetime.now()
                chat_id = message.chat.id
                date = (now.year, now.month)
                current_shown_dates[chat_id] = date
                markup = create_calendar(now.year, now.month)
                bot.send_message(message.chat.id, msg_refresh, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, close_chat)
        else:
            bot.send_message(message.chat.id, not_private_msg)
    except:
        pass


@bot.message_handler(commands=['invite'])
def send_welcome(message):
    try:
        if inchats(message.chat.id):
            link = '[' + invite_label  +'](https://telegram.me/' + telegrambot_name + '?start=' \
                   + select("select str from invite;")[0][0] + ')'
            bot.send_message(message.chat.id, msg_invite + link, parse_mode='MARKDOWN')
        else:
            bot.send_message(message.chat.id, close_chat)
    except:
        pass

@bot.message_handler(commands=['birthday'])
def send_welcome(message):
    try:
        if inchats(message.chat.id):
            bot.send_message(message.chat.id, birthday_list(), parse_mode='MARKDOWN', disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, close_chat)
    except:
        pass


@bot.message_handler(commands=['delete_user'])
def send_welcome(message):
    try:
        if inadminchats(message.chat.id):
            user_id = str(message.text)[13:]
            try:
                change("delete from chats where chat_id =" + user_id + ";")
                change("delete from status_sbor where chat_id=" + user_id + ";")
                bot.send_message(message.chat.id, success)
            except:
                pass
        else:
            bot.send_message(message.chat.id, not_support)
    except:
        pass

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    content_type = str(message.content_type)
    chat_id = message.chat.id

    if inadminchats(chat_id):
        logging.info("Incoming message on admin chat" + str(message) + " time:" + str(datetime.now()))
    else:
        logging.info("Incoming message on public chat" + str(message) + " time:" + str(datetime.now()))

    if content_type == 'text':
        change("update stats set number = number+1 where stat = 'messages';")
        text = str(message.text)
        if inadminchats(chat_id):
            if chat_id in ineventaccount:
                bot.send_chat_action(chat_id, 'typing')
                change("update events set account = '" + text + "' where status = 0;")
                bot.send_message(chat_id, success, reply_markup=adminmarkup)
                ineventaccount.remove(chat_id)
                if check_event():
                    bot.send_message(chat_id, event(),
                                     parse_mode='MARKDOWN',
                                     reply_markup=eventsendmarkup, disable_web_page_preview=True)
                else:
                    bot.send_message(chat_id, event(),
                                     parse_mode='MARKDOWN',
                                     reply_markup=eventmarkup, disable_web_page_preview=True)
            elif chat_id in ineventname:
                bot.send_chat_action(chat_id, 'typing')
                change("update events set name = '" + text + "' where status = 0;")
                bot.send_message(chat_id, success, reply_markup=adminmarkup)
                ineventname.remove(chat_id)
                if check_event():
                    bot.send_message(chat_id, event(),
                                     parse_mode='MARKDOWN',
                                     reply_markup=eventsendmarkup, disable_web_page_preview=True)
                else:
                    bot.send_message(chat_id, event(),
                                     parse_mode='MARKDOWN',
                                     reply_markup=eventmarkup, disable_web_page_preview=True)
            elif chat_id in ineventprice:
                bot.send_chat_action(chat_id, 'typing')
                change("update events set price = '" + text + "' where status = 0;")
                bot.send_message(chat_id, success, reply_markup=adminmarkup)
                ineventprice.remove(chat_id)
                if check_event():
                    bot.send_message(chat_id, event(),
                                     parse_mode='MARKDOWN',
                                     reply_markup=eventsendmarkup, disable_web_page_preview=True)
                else:
                    bot.send_message(chat_id, event(),
                                     parse_mode='MARKDOWN',
                                     reply_markup=eventmarkup, disable_web_page_preview=True)
            elif chat_id in ineventuser:
                if text != btn_list_user:
                    bot.send_chat_action(chat_id, 'typing')
                    id = str(text)
                    username = str(text)[1:]
                    row = select("select chat_id from chats where chat_id ='"
                               + id + "' or username = '" + username + "';")
                    if not row:
                        bot.send_message(chat_id, user_not_found)
                    else:
                        if select("select chat_id from u2e where chat_id = (select chat_id from chats where chat_id ='"
                               + id + "' or username = '" + username + "' limit 1) "
                                "and event_id = (select id from events where status = 0 limit 1);"):
                            change("delete from u2e where chat_id = (select chat_id from chats where chat_id ='"
                               + id + "' or username = '" + username + "' limit 1) "
                                "and event_id = (select id from events where status = 0 limit 1);")
                        else:
                            change("insert into u2e(chat_id, event_id) values((select chat_id from chats where chat_id ='"
                               + id + "' or username = '" + username + "'), (select id from events where "
                                "status = 0 limit 1));")
                    if check_event():
                        bot.send_message(chat_id, event(),
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventsendmarkup, disable_web_page_preview=True)
                    else:
                        bot.send_message(chat_id, event(),
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventmarkup, disable_web_page_preview=True)
                    ineventuser.remove(chat_id)
                else:
                    bot.send_chat_action(chat_id, 'typing')
                    bot.send_message(chat_id, users_list())
            elif text == btn_back:
                bot.send_chat_action(chat_id, 'typing')
                bot.send_message(chat_id, msg_back, reply_markup=adminmarkup)
            elif text == btn_static:
                bot.send_chat_action(chat_id, 'typing')
                stats = ""
                follow = ""
                for row in select("select (case when status = 0 then 'Пользователей' "
                            "else 'Администраторов' end) as label,count(chat_id) from chats group by label;"):
                        follow = follow + str(row[0]) + ": *" + str(row[1]) + "*\n"

                for row in select("select name, number from stats;"):
                    stats = str(row[0]) + ": *" + str(row[1]) + "*\n"
                reply = label_follow + \
                        follow + \
                        label_stats + \
                        stats
                bot.send_message(chat_id, reply, parse_mode='MARKDOWN', disable_web_page_preview=True)
            elif text == btn_event:
                bot.send_chat_action(chat_id, 'typing')
                bot.send_message(chat_id, msg_event,
                                 parse_mode='MARKDOWN',
                                 reply_markup=sboradminmarkup, disable_web_page_preview=True)
            elif text == btn_event_status:
                bot.send_chat_action(chat_id, 'typing')
                text = ""
                data = []
                for row in select("select st.name as st, s.status as s, count(*) "
                                  "from status_sbor s join statuses st on st.id = s.status group by st,s;"):
                    text = text + "*" +row[0] + ":* " + str(row[2]) + "\n"
                    data.append([row[0], str(row[1])])
                bot.send_message(chat_id, status_label + text, parse_mode='MARKDOWN',
                                 reply_markup=markup_callbackdata(data))
            elif text == btn_event_new:
                bot.send_chat_action(chat_id, 'typing')
                current_event = select("select name, price, account, rowid from events "
                                        "where status = 0 order by rowid desc limit 1;")
                if len(current_event) == 0:
                    change("INSERT INTO events(chat_id) VALUES (" + str(chat_id)+ ");")
                    bot.send_message(message.chat.id, event(), parse_mode='MARKDOWN',
                                     reply_markup=eventmarkup)
                else:
                    if check_event():
                        bot.send_message(chat_id, event(),
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventsendmarkup, disable_web_page_preview=True)
                    else:
                        bot.send_message(chat_id, event(),
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventmarkup, disable_web_page_preview=True)
            elif text == btn_list_user:
                bot.send_chat_action(chat_id, 'typing')
                bot.send_message(chat_id, users_list())
        else:
            if inchats(chat_id):
                if text == btn_url1:
                    bot.send_chat_action(chat_id, 'typing')
                    bot.send_message(chat_id, label_url1, parse_mode='MARKDOWN',
                                     reply_markup=url1markup, disable_web_page_preview=True)
                elif text == btn_url2:
                    bot.send_chat_action(chat_id, 'typing')
                    bot.send_message(chat_id, label_url2, parse_mode='MARKDOWN',
                                     reply_markup=url2markup, disable_web_page_preview=True)
                elif text == btn_url3:
                    bot.send_chat_action(chat_id, 'typing')
                    bot.send_message(chat_id, label_url3, parse_mode='MARKDOWN',
                                     reply_markup=url3markup, disable_web_page_preview=True)
            else:
                bot.send_message(chat_id, close_chat)


@bot.callback_query_handler(func=lambda call: call.data == 'event_cancel')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_cancel)
        bot.edit_message_text(msg_cancel_md, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'status_back')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        text = ""
        data = []
        for row in select("select st.name as st, s.status as s, count(*) "
                          "from status_sbor s join statuses st on st.id = s.status group by st,s;"):
            text = text + "*" + row[0] + ":* " + str(row[2]) + "\n"
            data.append([row[0], str(row[1])])
        bot.edit_message_text(status_label + text, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True,
                              reply_markup=markup_callbackdata(data))
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data[:7] == 'status-')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        text = ""
        status = call.data[7:]
        for row in select("select c.name, c.username, c.chat_id from chats c join status_sbor s on "
                          "c.chat_id = s.chat_id and s.status = " + str(status) + " where c.status = 0;"):
            text = text + prettyUsername(row[0], row[1]) + "\n"
        if status == '0':
            label_status = '*Не перевели*\n'
        elif status == '1':
            label_status = '*Перевели*\n'
        elif status == '2':
            label_status = '*Подтверждены*\n'
        elif status == '3':
            label_status = '*Виновники*\n'
        else:
            label_status = '*Другие*\n'
        bot.edit_message_text(label_status + text, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True,
                              reply_markup=statusbackmarkup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data[:15] == 'status_confirm-')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        id = call.data[15:]
        change("update status_sbor set status = 2 where chat_id = " + id + ";")
        bot.answer_callback_query(call.id, text=msg_thank_admin)
        bot.send_message(id, msg_confirm)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'sbor_send')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_thank)
        bot.edit_message_reply_markup(call.from_user.id,
                                      call.message.message_id)
        change("update status_sbor set status = 1 where chat_id = " + str(call.from_user.id) + ";")
        user = select("select chat_id, name, username from chats where chat_id=" + str(call.from_user.id) + ";")
        id = str(round(user[0][0]))
        user_text = prettyUsername(user[0][1], user[0][2])
        confirmmarkup = types.InlineKeyboardMarkup()
        row = []
        row.append(types.InlineKeyboardButton(text=btn_confirm, callback_data="status_confirm-" + id))
        confirmmarkup.row(*row)
        for chat in admin_list():
            bot.send_message(chat[0], label_pay_1 + user_text + label_pay_2, reply_markup=confirmmarkup,
                             parse_mode='MARKDOWN', disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_send')
def less_day(call):
    try:
        customer = prettyUsername(call.from_user.first_name, call.from_user.username)
        for row in select(
                "select name, price, account, id, rowid from events where "
                "status = 0 order by rowid desc limit 1;"):
            users = select("select name, username from chats where chat_id in "
                           "( select chat_id from u2e where event_id = " + str(row[3]) + ");")

            text = event(name=row[0], price=row[1], account=row[2],
                         users=users)
        user_to_send = []
        for row in select("select chat_id from chats where status = 0;"):
            user_to_send.append(row[0])
        for row in select("select chat_id from u2e where event_id = (select id from events where "
                            "status = 0 limit 1);"):
            user_to_send.remove(row[0])
        k = 0
        e = 0
        bot.answer_callback_query(call.id, text=sbor_complete)
        if user_to_send:
            for user in user_to_send:
                name = select("select name from chats where chat_id = " + str(user) + ";")
                try:
                    bot.send_message(user, hello(name[0][0]) + text,
                                     parse_mode='MARKDOWN',
                                     reply_markup=sbormarkup, disable_web_page_preview=True)
                    k = k + 1
                except:
                    e = e + 1
            bot.edit_message_text(text + sbor_complete_md + customer + count + str(k) + error_count + str(e),
                                  call.message.chat.id, call.message.message_id,
                                  parse_mode='MARKDOWN', disable_web_page_preview=True)
            change("update status_sbor set status = 0;")
            change("update status_sbor set status = 3 where chat_id in "
                   "(select chat_id from u2e where event_id = (select id from events where status = 0 limit 1));")
            change("update events set status = 1 where status = 0;")
        else:
            bot.edit_message_text(text + sbor_complete_md + empty_send_list, call.message.chat.id,
                                  call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)

    except:
        bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                              parse_mode='MARKDOWN')

@bot.callback_query_handler(func=lambda call: call.data == 'event_name')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        row = select("select id, rowid from events where status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventname.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_name_event, parse_mode='MARKDOWN', reply_markup = namemarkup,
                             disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_price')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        row = select("select id, rowid from events where status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventprice.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_price_event, parse_mode='MARKDOWN',
                             disable_web_page_preview=True, reply_markup=pricemarkup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_account')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        row = select("select id, rowid from events where status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventaccount.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_account_event, parse_mode='MARKDOWN',
                             disable_web_page_preview=True, reply_markup=accountmarkup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_user')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        row = select("select id, rowid from events where status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventuser.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_user_event, parse_mode='MARKDOWN',
                             disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day=call.data[13:]
        date = datetime(int(saved_date[0]), int(saved_date[1]), int(day))
        change("update chats set birthday = '" + str(date.strftime("%d.%m")) + "' where chat_id = "
                       + str(call.message.chat.id) + ";")
        bot.answer_callback_query(call.id, text=msg_done)
        bot.edit_message_text(start_msg_2, call.from_user.id, call.message.message_id,
                              parse_mode='MARKDOWN')
        bot.send_message(call.message.chat.id, msg_menu, reply_markup=startmarkup,
                         disable_web_page_preview=True)
    else:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text(call.message.text, call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text(call.message.text, call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text="")

try:
    for admin_chat_id in admin_list():
        bot.send_message(admin_chat_id[0], to_work_ready, reply_markup=adminmarkup)
except:
    pass

subprocess.Popen("python3 scheduler.py", shell=True)

while True:
    try:
        bot.polling()
    except:
        time.sleep(3)

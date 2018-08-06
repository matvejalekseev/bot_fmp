# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
from conf import *
from markups import *
from functions import *
from msg import *
import logging
from datetime import datetime
import time

logging.basicConfig(filename="logs/tele_bot.log", level=logging.INFO)

adminchatid = []
userchatid = []
ineventname = []
ineventaccount =[]
ineventprice = []
ineventuser = []

for row in select("select chat_id from chats where status = 1;"):
    adminchatid.append(float(row[0]))

for row in select("select chat_id from chats where status = 0;"):
    userchatid.append(float(row[0]))



bot = telebot.TeleBot(telegrambot_test)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        change("insert into chats(chat_id, username, name) values (" + str(message.chat.id) + ",'"
           + str(message.chat.username) + "','" +
           str(message.chat.last_name) + " " + str(message.chat.first_name) + "');")
        bot.send_message(message.chat.id, start_msg, reply_markup=startmarkup)
    else:
        bot.send_message(message.chat.id, not_private_msg)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    content_type = str(message.content_type)
    chat_type = str(message.chat.type)
    chat_id = message.chat.id

    if chat_id in adminchatid:
        logging.info("Incoming message on admin chat" + str(message) + " time:" + str(datetime.now()))
    else:
        logging.info("Incoming message on public chat" + str(message) + " time:" + str(datetime.now()))

    if content_type == 'text':
        change("update stats set number = number+1 where stat = 'messages';")
        text = str(message.text)
        if chat_id in adminchatid:
            if chat_id in ineventaccount:
                bot.send_chat_action(chat_id, 'typing')
                change("update events set account = '" + text + "' where status = 0;")
                ineventaccount.remove(chat_id)
                for row in select(
                        "select name, price, account, id, rowid from events where "
                        "status = 0 order by rowid desc limit 1;"):
                    users = select("select name, username from chats where chat_id in "
                                   "( select chat_id from u2e where event_id = " + str(row[3]) + ");")
                    text = event(name=row[0], price=row[1], account=row[2],
                                 users=users)
                    if check_event(row[0], row[1], row[2]):
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventsendmarkup, disable_web_page_preview=True)
                    else:
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventmarkup, disable_web_page_preview=True)
            elif chat_id in ineventname:
                bot.send_chat_action(chat_id, 'typing')
                change("update events set name = '" + text + "' where status = 0;")
                ineventname.remove(chat_id)
                for row in select(
                        "select name, price, account, id, rowid from events where "
                        "status = 0 order by rowid desc limit 1;"):
                    users = select("select name, username from chats where chat_id in "
                                   "( select chat_id from u2e where event_id = " + str(row[3]) + ");")
                    text = event(name=row[0], price=row[1], account=row[2],
                                 users=users)
                    if check_event(row[0], row[1], row[2]):
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventsendmarkup, disable_web_page_preview=True)
                    else:
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventmarkup, disable_web_page_preview=True)
            elif chat_id in ineventprice:
                bot.send_chat_action(chat_id, 'typing')
                change("update events set price = '" + text + "' where status = 0;")
                ineventprice.remove(chat_id)
                for row in select(
                        "select name, price, account, id, rowid from events where "
                        "status = 0 order by rowid desc limit 1;"):
                    users = select("select name, username from chats where chat_id in "
                                   "( select chat_id from u2e where event_id = " + str(row[3]) + ");")
                    text = event(name=row[0], price=row[1], account=row[2],
                                 users=users)
                    if check_event(row[0], row[1], row[2]):
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventsendmarkup, disable_web_page_preview=True)
                    else:
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventmarkup, disable_web_page_preview=True)
            elif chat_id in ineventuser:
                bot.send_chat_action(chat_id, 'typing')
                id = str(text)
                username = str(text)[1:]
                row = select("select chat_id from chats where chat_id ='"
                           + id + "' or username = '" + username + "';")
                if not row:
                    bot.send_message(chat_id, user_not_found + username)
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
                for row in select(
                        "select name, price, account, id, rowid from events where "
                        "status = 0 order by rowid desc limit 1;"):
                    users = select("select name, username from chats where chat_id in "
                                   "( select chat_id from u2e where event_id = " + str(row[3]) + ");")
                    text = event(name=row[0], price=row[1], account=row[2],
                                 users=users)
                    if check_event(row[0], row[1], row[2]):
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventsendmarkup, disable_web_page_preview=True)
                    else:
                        bot.send_message(chat_id, text,
                                         parse_mode='MARKDOWN',
                                         reply_markup=eventmarkup, disable_web_page_preview=True)
                ineventuser.remove(chat_id)
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
                current_event = select("select name, price, account, rowid from events "
                                        "where status = 0 order by rowid desc limit 1;")
                if len(current_event) == 0:
                    change("INSERT INTO events(chat_id) VALUES (" + str(chat_id)+ ");")
                    bot.send_message(message.chat.id, event(), parse_mode='MARKDOWN',
                                     reply_markup=eventmarkup)
                else:
                    for row in select(
                            "select name, price, account, id, rowid from events where "
                            "status = 0 order by rowid desc limit 1;"):
                        users = select("select name, username from chats where chat_id in "
                                       "( select chat_id from u2e where event_id = " + str(row[3]) + ");")
                        text = event(name=row[0], price=row[1], account=row[2],
                                     users=users)
                        if check_event(row[0], row[1], row[2]):
                            bot.send_message(chat_id, text,
                                             parse_mode='MARKDOWN',
                                             reply_markup=eventsendmarkup, disable_web_page_preview=True)
                        else:
                            bot.send_message(chat_id, text,
                                             parse_mode='MARKDOWN',
                                             reply_markup=eventmarkup, disable_web_page_preview=True)
            elif text == btn_list_user:
                bot.send_chat_action(chat_id, 'typing')
                text = ""
                users = select("select username,name,chat_id from chats where status = 0;")
                for user in users:
                    text = text + str(user[1]) + " " + "@" + str(user[0]) + " " + str(user[2]) + "\n"
                bot.send_message(message.chat.id, ladel_users + text, parse_mode='MARKDOWN')
        else:
            if text == btn_bg:
                bot.send_chat_action(chat_id, 'typing')
                bot.send_message(chat_id, in_work)
            elif text == btn_egisz:
                bot.send_chat_action(chat_id, 'typing')
                bot.send_message(chat_id, in_work)
            elif text == btn_adap:
                bot.send_chat_action(chat_id, 'typing')
                bot.send_message(chat_id, in_work)


@bot.callback_query_handler(func=lambda call: call.data == 'event_cancel')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=msg_cancel)
        bot.edit_message_text(msg_cancel_md, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_send')
def less_day(call):
    try:
        bot.answer_callback_query(call.id, text=sbor_complete)
        if call.from_user.username:
            customer = "[" + call.from_user.first_name \
                   + "](https://t.me/" + call.from_user.username + ")"
        else:
            customer = call.from_user.first_name

        for row in select(
                "select name, price, account, id, rowid from events where "
                "status = 0 order by rowid desc limit 1;"):
            users = select("select name, username from chats where chat_id in "
                           "( select chat_id from u2e where event_id = " + str(row[3]) + ");")

            text = event(name=row[0], price=row[1], account=row[2],
                         users=users)

        for row in select(
                "select name, price, account, id, rowid from events where "
                "status = 0 order by rowid desc limit 1;"):
            text_to_user = event(name=row[0], price=row[1], account=row[2])

        user_to_send = []
        for row in select("select chat_id from chats where status = 0;"):
            user_to_send.append(row[0])
        for row in select("select chat_id from u2e where event_id = (select id from events where "
                            "status = 0 limit 1);"):
            user_to_send.remove(row[0])
        k = 0
        if user_to_send:
            for user in user_to_send:
                k = k + 1
                name = select("select name from chats where chat_id = " + str(user) + ";")
                bot.send_message(user, hello(name[0][0]) + text_to_user,
                                 parse_mode='MARKDOWN',
                                 reply_markup=sbormarkup, disable_web_page_preview=True)
            bot.edit_message_text(text + sbor_complete_md + customer + count + str(k), call.message.chat.id,
                                      call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)
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
        row = select("select id, rowid from events where "
                    "status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventname.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_name_event, parse_mode='MARKDOWN',
                             disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_price')
def less_day(call):
    try:
        row = select("select id, rowid from events where "
                    "status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventprice.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_price_event, parse_mode='MARKDOWN',
                             disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_account')
def less_day(call):
    try:
        row = select("select id, rowid from events where "
                    "status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventaccount.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_account_event, parse_mode='MARKDOWN',
                             disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_user')
def less_day(call):
    try:
        row = select("select id, rowid from events where "
                    "status = 0 order by rowid desc limit 1;")
        if len(row) == 0:
            bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            ineventuser.append(call.message.chat.id)
            bot.send_message(call.message.chat.id, msg_user_event, parse_mode='MARKDOWN',
                             disable_web_page_preview=True)
    except:
        pass

try:
    for admin_chat_id in adminchatid:
        bot.send_chat_action(admin_chat_id, 'typing')
        bot.send_message(admin_chat_id, to_work_ready, reply_markup=adminmarkup)
except:
    pass

while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)

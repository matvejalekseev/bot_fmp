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
            if text == btn_static:
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
                                       "( select chat_id from u2e where event_id = " + row[3] + ");")
                        text = event(name=row[0], price=row[1], account=row[2],
                                     users=users)
                        if check_event(row[0], row[1], row[2]):
                            bot.send_message(chat_id, text,
                                             parse_mode='MARKDOWN',
                                             reply_markup=eventsendmarkup)
                        else:
                            bot.send_message(chat_id, text,
                                             parse_mode='MARKDOWN',
                                             reply_markup=eventmarkup)
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

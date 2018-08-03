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

    change("insert into chats(chat_id, username, name) values (" + str(message.chat.id) + ");")
    bot.send_message(message.chat.id, start_msg, reply_markup=startmarkup)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    content_type = str(message.content_type)
    chat_type = str(message.chat.type)
    chat_id = message.chat.id

    change("update stats set number = number+1 where stat = 'messages';")


    if chat_id in adminchatid:
        logging.info("Incoming message on admin chat" + str(message) + " time:" + str(datetime.now()))
    else:
        logging.info("Incoming message on public chat" + str(message) + " time:" + str(datetime.now()))

    if content_type == 'text':
        text = str(message.text)
        if chat_id in adminchatid:
            if text == 'Статистика':
                bot.send_chat_action(chat_id, 'typing')
                label_follow = '*На меня подписано:*\n'
                for row in select(
                            "select (case when status = 0 then 'Пользователей' "
                            "else 'Администраторов' end) as label,count(chat_id) from chats group by label;"):
                        label_follow = label_follow + str(row[0]) + ": *" + str(row[1]) + "*\n"

                label_stats = '*Показатели:*\n'
                stats = ""
                for row in select(
                            "select name, number from stats;"):
                        stats = str(row[0]) + ": *" + str(row[1]) + "*\n"

                reply = label_follow + "\n" + \
                        label_stats + \
                        stats

                bot.send_message(chat_id, reply, parse_mode='MARKDOWN', disable_web_page_preview=True)
        else:
            bot.send_chat_action(chat_id, 'typing')

try:
    for admin_chat_id in adminchatid:
        bot.send_chat_action(admin_chat_id, 'typing')
        bot.send_message(admin_chat_id, "Я запущен!", reply_markup=adminmarkup)
except:
    pass

while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)

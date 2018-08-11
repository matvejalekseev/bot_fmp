import time
from random import choice
from string import ascii_uppercase
import schedule
import telebot
from conf import *
from functions import *
from msg import *


def invite():
    try:
        new_str = ''.join(choice(ascii_uppercase) for i in range(12))
        change("update invite set str = '" + new_str + "';")
    except:
        pass

def job_time():
    try:
        current_day = datetime.now().day
        if current_day in jira_sched_day:
            for chat in select("select chat_id from chats where status = 0;"):
                try:
                    bot.send_message(chat[0], msg_time_jira, parse_mode='MARKDOWN', disable_web_page_preview=True)
                except:
                    pass
    except:
        pass


def job_bd():
    try:
        day = datetime.now().day
        current_db = select("select name,username,chat_id from chats where status = 0 "
                            "and birthday = '" + current_date() + "';")
        for chat in current_db:
            bot.send_message(chat[2], prettyUsername(chat[0], chat[1]) + msg_gratz,
                             parse_mode='MARKDOWN', disable_web_page_preview=True)
        if day in bd_sched_day:
            for chat in select("select chat_id from chats where status = 0;"):
                try:
                    bot.send_message(chat[0], birthday_list(), parse_mode='MARKDOWN', disable_web_page_preview=True)
                except:
                    pass
    except:
        pass

schedule.every().day.at(bd_sched_time).do(job_time)
schedule.every().day.at(jira_sched_time).do(job_bd)
schedule.every().day.at(invite_sched_time).do(invite)

bot = telebot.TeleBot(telegrambot_test)

while True:
    try:
        schedule.run_pending()
        time.sleep(10)
    except:
        pass

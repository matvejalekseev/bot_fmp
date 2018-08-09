import telebot
from conf import *
from functions import *
from msg import *
from datetime import datetime
import time
import schedule
from random import choice
from string import ascii_uppercase



def invite():
    new_str = ''.join(choice(ascii_uppercase) for i in range(12))
    change("update invite set str = '" + new_str + "';")

def job_time():
    current_day = datetime.now().day
    if current_day in jira_sched_day:
        for chat in select("select chat_id from chats where status = 0;"):
            try:
                bot.send_message(chat[0], msg_time_jira, parse_mode='MARKDOWN', disable_web_page_preview=True)
            except:
                pass


def job_bd():
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
    current_date = current_day + '.' + current_month
    current_db = select("select name,username,chat_id from chats where status = 0 "
                        "and birthday = '" + current_date + "';")
    for chat in current_db:
        bot.send_message(chat[2], prettyUsername(chat[0], chat[1]) + msg_gratz,
                         parse_mode='MARKDOWN', disable_web_page_preview=True)
    if current_day in bd_sched_day:
        text = ""
        for bd in select("select birthday,name,username from chats where status = 0;"):
            birthday = bd[0]
            if birthday[3:] == current_month:
                text = text + birthday[:2] + " - " + prettyUsername(bd[1], bd[2]) + "\n"
        for chat in select("select chat_id from chats where status = 0;"):
            try:
                bot.send_message(chat[0], db_label + text, parse_mode='MARKDOWN',disable_web_page_preview=True)
            except:
                pass

schedule.every().day.at(bd_sched_time).do(job_time)
schedule.every().day.at(jira_sched_time).do(job_bd)
schedule.every().day.at(invite_sched_time).do(invite)

bot = telebot.TeleBot(telegrambot_test)

while True:
    schedule.run_pending()
    time.sleep(15)
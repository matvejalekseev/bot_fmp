import telebot
from conf import *
from functions import *
from msg import *
from datetime import datetime
import time
import schedule

def job_time():
    for chat in select("select chat_id from chats where status = 0;"):
        bot.send_message(chat[0], msg_time_jira, parse_mode='MARKDOWN', disable_web_page_preview=True)


def job_bd():
    current_day = datetime.now().day
    current_month = datetime.now().month
    if current_day == 6:
        text = ""
        for bd in select("select birthday,name,username from chats where status = 0;"):
            birthday = bd[0]
            if birthday[3:] == str(current_month) or birthday[3:] == '0'+str(current_month):
                text = text + birthday[:2] + " - [" + bd[1] + "](https://t.me/" + bd[2] + ")\n"
        for chat in select("select chat_id from chats where status = 0;"):
            bot.send_message(chat[0], db_label + text, parse_mode='MARKDOWN',disable_web_page_preview=True)

schedule.every().day.at(bd_sched_time).do(job_time)
schedule.every().day.at(jira_sched_time).do(job_bd)

bot = telebot.TeleBot(telegrambot_test)

while True:
    schedule.run_pending()
    time.sleep(15)
import time
from random import choice
from string import ascii_uppercase
import schedule
import telebot
from conf import *
from functions import *
from msg import *
from markups import *


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
            for chat in user_list():
                try:
                    bot.send_message(chat[0], msg_time_jira, parse_mode='MARKDOWN', disable_web_page_preview=True,
                                     reply_markup=likemarkup)
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
                             parse_mode='MARKDOWN', disable_web_page_preview=True, reply_markup=likemarkup)
            change_stats(1, 'gratz')
        if day in bd_sched_day:
            for chat in select("select chat_id from chats where status = 0;"):
                try:
                    bot.send_message(chat[0], birthday_list(), parse_mode='MARKDOWN', disable_web_page_preview=True)
                except:
                    pass
    except:
        pass

def job_event_reminder():
    try:
        if not all_event_end():
            for chat in list_users_to_remind():
                bot.send_message(chat[0], msg_remind + event_in_proccess(),
                                 parse_mode='MARKDOWN', disable_web_page_preview=True)
                change_stats(1, 'remind')
    except:
        pass

def job_holyday_start():
    try:
        start = select("select chat_id from holidays where action = 'start' and date = '" + current_date_with_year() + "';")
        for chat in start:
            bot.send_message(chat[0], msg_holiday_start_gratz,
                             parse_mode='MARKDOWN', disable_web_page_preview=True)
            change_stats(1, 'holiday')
            change("update status_sbor set status = 4 where chat_id = " + str(chat[0]) + ";")
            change("delete from holidays where action = 'start' and chat_id = " + str(chat[0]) + ";")
    except:
        pass

def job_holyday_stop():
    try:
        stop = select("select chat_id from holidays where action = 'stop' and date = '" + current_date_with_year() + "';")
        for chat in stop:
            bot.send_message(chat[0], msg_holiday_stop_gratz,
                             parse_mode='MARKDOWN', disable_web_page_preview=True)
            change_stats_down(1, 'holiday')
            change("update status_sbor set status = 0 where chat_id = " + str(chat[0]) + ";")
            change("delete from holidays where action = 'stop' and chat_id = " + str(chat[0]) + ";")
    except:
        pass

schedule.every().day.at(bd_sched_time).do(job_time)
schedule.every().day.at(jira_sched_time).do(job_bd)
schedule.every().day.at(invite_sched_time).do(invite)
schedule.every().day.at(event_reminder_sched_time).do(job_event_reminder)
schedule.every().day.at(holyday_start_time).do(job_holyday_start)
schedule.every().day.at(holyday_stop_time).do(job_holyday_stop)

bot = telebot.TeleBot(telegrambot_test)

while True:
    try:
        schedule.run_pending()
        time.sleep(10)
    except:
        pass

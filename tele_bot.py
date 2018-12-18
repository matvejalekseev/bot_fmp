import logging
import subprocess
import time
import telebot
from conf import *
from functions import *
from markups import *
from msg import *
from telegramcalendar import *

logging.basicConfig(filename="logs/tele_bot.log", level=logging.INFO)

current_shown_dates={}

ineventname = []
ineventaccount =[]
ineventprice = []
ineventuser = []
insetmessage = []
insetholidaystep1 = []
insetholidaystep2 = []

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
                user_text = prettyUsername(prettyPrintName(message.chat.last_name, message.chat.first_name),
                                           str(message.chat.username))
                for chat in admin_list():
                    bot.send_message(chat[0], msg_new_user + user_text,
                                     parse_mode='MARKDOWN', disable_web_page_preview=True)
                date = (now.year, now.month)
                current_shown_dates[chat_id] = date
                markup = create_calendar(now.year, now.month)
                bot.send_message(message.chat.id, start_msg, reply_markup=markup)
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

@bot.message_handler(commands=['holiday'])
def send_welcome(message):
    try:
        if inchats(message.chat.id):
            if message.chat.type == 'private':
                if inholiday(message.chat.id):
                    bot.send_message(message.chat.id, holiday_list(), reply_markup=inholidaymarkup,
                                     parse_mode='MARKDOWN', disable_web_page_preview=True)
                elif holidayexists(message.chat.id):
                    bot.send_message(message.chat.id, holiday_list(), reply_markup=holidayexistsmarkup,
                                     parse_mode='MARKDOWN', disable_web_page_preview=True)
                else:
                    bot.send_message(message.chat.id, holiday_list(), reply_markup=holidaymarkup,
                                     parse_mode='MARKDOWN', disable_web_page_preview=True)
            else:
                bot.send_message(message.chat.id, holiday_list(), parse_mode='MARKDOWN', disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, close_chat)
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


@bot.message_handler(commands=['check_users'])
def send_welcome(message):
    try:
        if inadminchats(message.chat.id):
            text = ''
            for chat in user_list_with_name():
                try:
                    bot.send_chat_action(chat[0], 'typing')
                except:
                    text = text + '<a href="tg://user?id=' + str(round(chat[0])) + '">' + chat[1] + '</a>\n'
            bot.send_message(message.chat.id, 'От меня отписались:\n' + text, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, not_support)
    except:
        pass


@bot.message_handler(commands=['confirm'])
def send_welcome(message):
    try:
        if inadminchats(message.chat.id):
            if all_event_end():
                bot.send_message(message.chat.id, msg_no_open_event)
            else:
                user_id = str(message.text)[9:]
                try:
                    change("update status_sbor set status = 2 where chat_id = " + user_id + ";")
                    bot.send_message(message.chat.id, success)
                    bot.send_message(user_id, msg_confirm)
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
        change_stats(1, 'messages')
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
            elif chat_id in insetmessage:
                if text != btn_mass_send:
                    bot.send_message(chat_id, mass_send_label + text,
                                          reply_markup=masssendmarkup, disable_web_page_preview=True)
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
                    stats = stats + str(row[0]) + ": *" + str(row[1]) + "*\n"
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
                bot.send_message(chat_id, status_label + event_status() + text, parse_mode='MARKDOWN',
                                 reply_markup=markup_callbackdata(data))
            elif text == btn_event_new:
                bot.send_chat_action(chat_id, 'typing')
                if all_event_end():
                    current_event = select("select name, price, account, rowid from events "
                                           "where status = 0 order by rowid desc limit 1;")
                    if len(current_event) == 0:
                        change("INSERT INTO events(chat_id) VALUES (" + str(chat_id) + ");")
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
                else:
                    bot.send_message(message.chat.id, msg_event_not_end, parse_mode='MARKDOWN')
            elif text == btn_list_user:
                bot.send_chat_action(chat_id, 'typing')
                bot.send_message(chat_id, users_list())
            elif text == btn_event_end:
                bot.send_chat_action(chat_id, 'typing')
                if not all_event_end():
                    id = str(select("select id from events where status = 1;")[0][0])
                    sborendconfirmmarkup = types.InlineKeyboardMarkup()
                    row = []
                    row.append(types.InlineKeyboardButton(text=btn_yes, callback_data="sbor_confirm-" + id))
                    row.append(types.InlineKeyboardButton(text=btn_no, callback_data="sbor_confirm_no"))
                    sborendconfirmmarkup.row(*row)
                    bot.send_message(chat_id, msg_event_end_confirm,
                                     parse_mode='MARKDOWN',
                                     reply_markup=sborendconfirmmarkup, disable_web_page_preview=True)
                else:
                    bot.send_message(message.chat.id, msg_no_open_event, parse_mode='MARKDOWN')
            elif text == btn_mass_send:
                    insetmessage.append(chat_id)
                    bot.send_message(chat_id, msg_mass_send, reply_markup=stopmasssendmarkup,
                                     disable_web_page_preview=True)
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
def event_cancel(call):
    try:
        bot.answer_callback_query(call.id, text=msg_cancel)
        bot.edit_message_text(msg_cancel_md, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_mass_send')
def cancel_mass_send(call):
    try:
        bot.answer_callback_query(call.id, text=msg_cancel)
        bot.edit_message_text(msg_cancel_mass_send, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)
        insetmessage.remove(call.message.chat.id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'status_back')
def status_back(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        text = ""
        data = []
        for row in select("select st.name as st, s.status as s, count(*) "
                          "from status_sbor s join statuses st on st.id = s.status group by st,s;"):
            text = text + "*" + row[0] + ":* " + str(row[2]) + "\n"
            data.append([row[0], str(row[1])])
        bot.edit_message_text(status_label + event_status() + text, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True,
                              reply_markup=markup_callbackdata(data))
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data[:7] == 'status-')
def status(call):
    try:
        bot.answer_callback_query(call.id, text=msg_done)
        text = ""
        status = call.data[7:]
        for row in select("select c.name, c.username, c.chat_id from chats c join status_sbor s on "
                          "c.chat_id = s.chat_id and s.status = " + str(status) + " where c.status = 0;"):
            text = text + prettyUsername(row[0], row[1]) + " ```" + str(round(row[2])) + "```\n"
        label_status = '*' + statusName(status) + '*\n'
        bot.edit_message_text(label_status + text, call.message.chat.id,
                          call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True,
                              reply_markup=statusbackmarkup)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data[:13] == 'sbor_confirm-')
def sbor_confirm(call):
    try:
        if all_event_end():
            bot.answer_callback_query(call.id, text=msg_sbor_is_over)
        else:
            id = call.data[13:]
            change("update events set status = 2 where id = " + id + ";")
            bot.answer_callback_query(call.id, text=msg_done)
            bot.edit_message_text(msg_event_end_done, call.message.chat.id,
                                  call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'sbor_confirm_no')
def sbor_confirm_no(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data[:15] == 'status_confirm-')
def status_confirm(call):
    try:
        if all_event_end():
            bot.answer_callback_query(call.id, text=msg_sbor_is_over)
            bot.edit_message_reply_markup(call.from_user.id,
                                          call.message.message_id)
        else:
            bot.answer_callback_query(call.id, text=msg_done)
            id = call.data[15:]
            change("update status_sbor set status = 2 where chat_id = " + id + ";")
            bot.answer_callback_query(call.id, text=msg_thank_admin)
            bot.send_message(id, msg_confirm)
            bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data[:10] == 'sbor_send-')
def sbor_send(call):
    try:
        sbor_id = call.data[10:]
        if is_open_event(sbor_id):
            if is_proccess__user_event(call.from_user.id):
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
            else:
                bot.answer_callback_query(call.id, text=msg_sbor_is_confirm)
                bot.edit_message_reply_markup(call.from_user.id,
                                              call.message.message_id)
        else:
            bot.answer_callback_query(call.id, text=msg_sbor_is_over)
            bot.edit_message_reply_markup(call.from_user.id,
                                          call.message.message_id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'event_send')
def event_send(call):
    try:
        customer = prettyUsername(call.from_user.first_name, call.from_user.username)
        user_to_send = []
        for row in user_list_to_send():
            user_to_send.append(row[0])
        try:
            for row in select("select chat_id from u2e where event_id = (select id from events where "
                            "status = 0 limit 1);"):
                user_to_send.remove(row[0])
        except:
            pass
        k = 0
        e = 0
        bot.answer_callback_query(call.id, text=sbor_complete)
        if user_to_send:
            callback_data = "sbor_send-" + str(select("select id from events where status = 0 limit 1")[0][0])
            sbormarkup = types.InlineKeyboardMarkup()
            row = []
            row.append(types.InlineKeyboardButton(text=btn_sbor, callback_data=callback_data))
            sbormarkup.row(*row)
            for user in user_to_send:
                name = select("select name from chats where chat_id = " + str(user) + ";")
                try:
                    bot.send_message(user, hello(name[0][0]) + event(),
                                     parse_mode='MARKDOWN',
                                     reply_markup=sbormarkup, disable_web_page_preview=True)
                    k = k + 1
                except:
                    e = e + 1
            bot.edit_message_text(event() + sbor_complete_md + customer + count + str(k) + error_count + str(e),
                                  call.message.chat.id, call.message.message_id,
                                  parse_mode='MARKDOWN', disable_web_page_preview=True)
            change_stats(k, 'event')
            change_stats(e, 'eventError')
            change("update status_sbor set status = 0 where status <> 4;")
            change("update status_sbor set status = 3 where chat_id in "
                   "(select chat_id from u2e where event_id = (select id from events where status = 0 limit 1)) "
                   "and status <> 4;")
            change("update events set status = 1 where status = 0;")
        else:
            bot.edit_message_text(event() + sbor_complete_md + empty_send_list, call.message.chat.id,
                                  call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)

    except:
        bot.edit_message_text(msg_start_new, call.from_user.id, call.message.message_id,
                              parse_mode='MARKDOWN')

@bot.callback_query_handler(func=lambda call: call.data == 'event_name')
def event_name(call):
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
def event_price(call):
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
def event_account(call):
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
def event_user(call):
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

@bot.callback_query_handler(func=lambda call: call.data == 'send_mass')
def send_mass(call):
    bot.answer_callback_query(call.id, text=msg_done)
    try:
        k = 0
        e = 0
        text = call.message.text.lstrip(mass_send_label)
        for row in user_list_with_name():
            try:
                bot.send_message(row[0], hello(row[1])  + text,
                         parse_mode='MARKDOWN', disable_web_page_preview=True, reply_markup=likemarkup)
                k = k + 1
            except:
                e = e + 1
        change_stats(k, 'mass_messages')
        change_stats(e, 'mass_messages_error')
        text = mass_send_label_done + text + count + str(k) + error_count + str(e) + "\n" +\
               prettyUsername(prettyPrintName(call.from_user.last_name, call.from_user.first_name),
                              call.from_user.username)
        bot.edit_message_text(text, call.message.chat.id,
                              call.message.message_id, parse_mode='MARKDOWN', disable_web_page_preview=True)
        insetmessage.remove(call.message.chat.id)
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'like')
def like(call):
    change_stats(1, 'likes')
    bot.answer_callback_query(call.id, text=msg_thank_for_like)
    bot.edit_message_reply_markup(call.from_user.id,
                          call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'dislike')
def dislike(call):
    change_stats(1, 'dislikes')
    bot.answer_callback_query(call.id, text=msg_thank_for_like)
    bot.edit_message_reply_markup(call.from_user.id,
                          call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day = call.data[13:]
        date_in = datetime(int(saved_date[0]), int(saved_date[1]), int(day))
        if call.message.chat.id in insetholidaystep1:
            change("insert into holidays(chat_id,date) values (" + str(call.from_user.id) + ", '"
                   + str(date_in.strftime("%d.%m.%Y")) + "');")
            now = datetime.now()
            date = (now.year, now.month)
            current_shown_dates[call.from_user.id] = date
            markup = create_calendar_with_year_to_future(now.year, now.month)
            insetholidaystep1.remove(call.from_user.id)
            insetholidaystep2.append(call.from_user.id)
            bot.edit_message_text(msg_holiday_step_2, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN', reply_markup=markup)
        elif call.message.chat.id in insetholidaystep2:
            update_stop_holiday_date(call.from_user.id, str(date_in.strftime("%d.%m.%Y")))
            insetholidaystep2.remove(call.from_user.id)
            bot.edit_message_text(msg_holiday_done, call.from_user.id, call.message.message_id,
                                  parse_mode='MARKDOWN')
        else:
            change("update chats set birthday = '" + str(date_in.strftime("%d.%m")) + "' where chat_id = "
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
        if chat_id in insetholidaystep1 or chat_id in insetholidaystep2:
            markup = create_calendar_with_year_to_future(year, month)
        else:
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
        if chat_id in insetholidaystep1 or chat_id in insetholidaystep2:
            markup = create_calendar_with_year_to_future(year, month)
        else:
            markup= create_calendar(year,month)
        bot.edit_message_text(call.message.text, call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text="")

@bot.callback_query_handler(func=lambda call: call.data == 'less_day')
def less_day(call):
    bot.answer_callback_query(call.id, text=msg_less_day)

@bot.callback_query_handler(func=lambda call: call.data == 'holiday_refresh')
def holiday_refresh(call):
    now = datetime.now()
    date = (now.year, now.month)
    current_shown_dates[call.from_user.id] = date
    markup = create_calendar_with_year_to_future(now.year, now.month)
    insetholidaystep1.append(call.from_user.id)
    bot.send_message(call.from_user.id, msg_holiday_start, reply_markup=markup)
    change("delete from holidays where chat_id = " + str(call.from_user.id) + ";")
    bot.edit_message_reply_markup(call.from_user.id,
                                  call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'holiday_delete')
def holiday_delete(call):
    change("delete from holidays where chat_id = " + str(call.from_user.id) + ";")
    change("delete from holidays where action = 'stop' and chat_id = " + str(call.from_user.id) + ";")
    bot.edit_message_reply_markup(call.from_user.id,
                                  call.message.message_id)
    bot.send_message(call.from_user.id, msg_holiday_deleted)

@bot.callback_query_handler(func=lambda call: call.data == 'holiday_end')
def holiday_end(call):
    change("update status_sbor set status = 5 where chat_id = " + str(call.from_user.id) + ";")
    change("delete from holidays where chat_id = " + str(call.from_user.id) + ";")
    change_stats_down(1, 'holiday')
    bot.edit_message_reply_markup(call.from_user.id,
                                  call.message.message_id)
    bot.send_message(call.from_user.id, msg_holiday_ended)


try:
    for admin_chat_id in admin_list():
        bot.send_message(admin_chat_id[0], to_work_ready, reply_markup=adminmarkup)
except:
    pass

subprocess.Popen("python3.5 scheduler.py", shell=True)

while True:
    try:
        bot.polling()
    except:
        time.sleep(3)

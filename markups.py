from telebot import types
from msg import *

startmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_url1)
itembtn2 = types.KeyboardButton(btn_url2)
itembtn3 = types.KeyboardButton(btn_url3)
startmarkup.add(itembtn1, itembtn2, itembtn3)

pricemarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_100)
itembtn2 = types.KeyboardButton(btn_150)
itembtn3 = types.KeyboardButton(btn_250)
pricemarkup.add(itembtn1, itembtn2, itembtn3)

namemarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_bd)
itembtn2 = types.KeyboardButton(btn_wending)
itembtn3 = types.KeyboardButton(btn_kid)
itembtn4 = types.KeyboardButton(btn_bye)
namemarkup.add(itembtn1, itembtn2, itembtn3, itembtn4)

accountmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_default_account)
accountmarkup.add(itembtn1)

adminmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_event)
itembtn2 = types.KeyboardButton(btn_mass_send)
itembtn3 = types.KeyboardButton(btn_static)
itembtn4 = types.KeyboardButton(btn_list_user)
adminmarkup.add(itembtn1, itembtn2, itembtn3, itembtn4)

sboradminmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_event_status)
itembtn2 = types.KeyboardButton(btn_event_new)
itembtn3 = types.KeyboardButton(btn_event_end)
itembtn4 = types.KeyboardButton(btn_back)
sboradminmarkup.add(itembtn1, itembtn2, itembtn3, itembtn4)

statusbackmarkup = types.InlineKeyboardMarkup()
row=[]
row.append(types.InlineKeyboardButton(text=btn_status_back, callback_data="status_back"))
statusbackmarkup.row(*row)

eventmarkup = types.InlineKeyboardMarkup()
row=[]
row.append(types.InlineKeyboardButton(text=btn_name, callback_data="event_name"))
row.append(types.InlineKeyboardButton(text=btn_price, callback_data="event_price"))
eventmarkup.row(*row)
row=[]
row.append(types.InlineKeyboardButton(text=btn_account, callback_data="event_account"))
row.append(types.InlineKeyboardButton(text=btn_user, callback_data="event_user"))
eventmarkup.row(*row)
row=[]
row.append(types.InlineKeyboardButton(text=btn_cancel, callback_data="event_cancel"))
eventmarkup.row(*row)

eventsendmarkup = types.InlineKeyboardMarkup()
row=[]
row.append(types.InlineKeyboardButton(text=btn_name, callback_data="event_name"))
row.append(types.InlineKeyboardButton(text=btn_price, callback_data="event_price"))
eventsendmarkup.row(*row)
row=[]
row.append(types.InlineKeyboardButton(text=btn_account, callback_data="event_account"))
row.append(types.InlineKeyboardButton(text=btn_user, callback_data="event_user"))
eventsendmarkup.row(*row)
row=[]
row.append(types.InlineKeyboardButton(text=btn_cancel, callback_data="event_cancel"))
eventsendmarkup.row(*row)
row=[]
row.append(types.InlineKeyboardButton(text=btn_send, callback_data="event_send"))
eventsendmarkup.row(*row)

url1markup = types.InlineKeyboardMarkup()
for url in url_1:
    url1markup.add(types.InlineKeyboardButton(text=url[0], url=url[1]))

url2markup = types.InlineKeyboardMarkup()
for url in url_2:
    url2markup.add(types.InlineKeyboardButton(text=url[0], url=url[1]))

url3markup = types.InlineKeyboardMarkup()
for url in url_3:
    url3markup.add(types.InlineKeyboardButton(text=url[0], url=url[1]))

stopmasssendmarkup = types.InlineKeyboardMarkup()
stopmasssendmarkup.add(types.InlineKeyboardButton(text=btn_mass_send_back, callback_data="cancel_mass_send"))

masssendmarkup = types.InlineKeyboardMarkup()
masssendmarkup.add(types.InlineKeyboardButton(text=btn_mass_send_ok, callback_data="send_mass"))
masssendmarkup.add(types.InlineKeyboardButton(text=btn_mass_send_back, callback_data="cancel_mass_send"))

likemarkup = types.InlineKeyboardMarkup()
row=[]
row.append(types.InlineKeyboardButton(text=btn_like, callback_data="like"))
row.append(types.InlineKeyboardButton(text=btn_dislike, callback_data="dislike"))
likemarkup.row(*row)



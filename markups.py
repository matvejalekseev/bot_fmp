from telebot import types
from msg import *


sharemarkup = types.InlineKeyboardMarkup()
row=[]
row.append(types.InlineKeyboardButton(text='Share with your friends', switch_inline_query='share'))
sharemarkup.row(*row)

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
itembtn2 = types.KeyboardButton(btn_static)
itembtn3 = types.KeyboardButton(btn_list_user)
adminmarkup.add(itembtn1, itembtn2, itembtn3)

sboradminmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_event_status)
itembtn2 = types.KeyboardButton(btn_event_new)
itembtn3 = types.KeyboardButton(btn_back)
sboradminmarkup.add(itembtn1, itembtn2, itembtn3)

statusmarkup = types.InlineKeyboardMarkup()
row=[]
row.append(types.InlineKeyboardButton(text=btn_status1, callback_data="status1"))
row.append(types.InlineKeyboardButton(text=btn_status2, callback_data="status2"))
statusmarkup.row(*row)
row=[]
row.append(types.InlineKeyboardButton(text=btn_status3, callback_data="status3"))
row.append(types.InlineKeyboardButton(text=btn_status4, callback_data="status4"))
statusmarkup.row(*row)

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

sbormarkup = types.InlineKeyboardMarkup()
row=[]
row.append(types.InlineKeyboardButton(text=btn_sbor, callback_data="sbor_send"))
sbormarkup.row(*row)

url1markup = types.InlineKeyboardMarkup()
for url in url_1:
    url1markup.add(types.InlineKeyboardButton(text=url[0], url=url[1]))

url2markup = types.InlineKeyboardMarkup()
for url in url_2:
    url2markup.add(types.InlineKeyboardButton(text=url[0], url=url[1]))

url3markup = types.InlineKeyboardMarkup()
for url in url_3:
    url3markup.add(types.InlineKeyboardButton(text=url[0], url=url[1]))


#Примеры
elementmarkup_soc = types.InlineKeyboardMarkup()
elementmarkup_soc.add(types.InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/element_show"))
elementmarkup_soc.add(types.InlineKeyboardButton(text="ВКонтакте", url="https://vk.com/club92907131"))
elementmarkup_soc.add(types.InlineKeyboardButton(text="Официальный сайт", url="http://elementshow.com"))


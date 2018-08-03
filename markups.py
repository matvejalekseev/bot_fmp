from telebot import types
from msg import *

startmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_bg)
itembtn2 = types.KeyboardButton(btn_egisz)
itembtn3 = types.KeyboardButton(btn_adap)
startmarkup.add(itembtn1, itembtn2, itembtn3)

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
eventsendmarkup.row(*row)

#Примеры
elementmarkup_soc = types.InlineKeyboardMarkup()
elementmarkup_soc.add(types.InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/element_show"))
elementmarkup_soc.add(types.InlineKeyboardButton(text="ВКонтакте", url="https://vk.com/club92907131"))
elementmarkup_soc.add(types.InlineKeyboardButton(text="Официальный сайт", url="http://elementshow.com"))

adminmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton(btn_event)
itembtn2 = types.KeyboardButton(btn_static)
itembtn3 = types.KeyboardButton(btn_list_user)
adminmarkup.add(itembtn1, itembtn2, itembtn3)


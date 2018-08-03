from telebot import types

startmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('Полезные ссылки БГ')
itembtn2 = types.KeyboardButton('Полезные ссылки ЕГИСЗ')
itembtn3 = types.KeyboardButton('Адаптация')
startmarkup.add(itembtn1, itembtn2, itembtn3)


#Примеры
elementmarkup_soc = types.InlineKeyboardMarkup()
elementmarkup_soc.add(types.InlineKeyboardButton(text="Instagram", url="https://www.instagram.com/element_show"))
elementmarkup_soc.add(types.InlineKeyboardButton(text="ВКонтакте", url="https://vk.com/club92907131"))
elementmarkup_soc.add(types.InlineKeyboardButton(text="Официальный сайт", url="http://elementshow.com"))

adminmarkup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('Массовая рассылка')
itembtn2 = types.KeyboardButton('Статистика')
adminmarkup.add(itembtn1, itembtn2)


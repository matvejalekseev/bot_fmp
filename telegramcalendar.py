from telebot import types
import calendar
import locale
from datetime import datetime



def create_calendar(year,month):
    markup = types.InlineKeyboardMarkup()
    #First row - Month and Year
    row=[]
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    row.append(types.InlineKeyboardButton(calendar.month_name[month],callback_data="ignore"))
    markup.row(*row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week:
            if(day==0):
                row.append(types.InlineKeyboardButton(" ",callback_data="ignore"))
            else:
                now = datetime.now()
                if datetime.strptime(str(now.day) + "." + str(now.month) + "." + str(now.year), "%d.%m.%Y") <= datetime.strptime(
                        str(day) + "." + str(month) + "." + str(year), "%d.%m.%Y"):
                    row.append(types.InlineKeyboardButton(str(day),callback_data="calendar-day-"+str(day)))
                else:
                    row.append(types.InlineKeyboardButton(str(day), callback_data="less_day"))
        markup.row(*row)
    #Last row - Buttons
    row=[]
    now = datetime.now()
    if datetime.strptime(str(now.month)+"."+str(now.year), "%m.%Y") < datetime.strptime(str(month)+"."+str(year), "%m.%Y"):
        row.append(types.InlineKeyboardButton("<",callback_data="previous-month"))
    else:
        row.append(types.InlineKeyboardButton(" ", callback_data="ignore"))
    row.append(types.InlineKeyboardButton(" ",callback_data="ignore"))
    row.append(types.InlineKeyboardButton(">",callback_data="next-month"))
    markup.row(*row)
    return markup
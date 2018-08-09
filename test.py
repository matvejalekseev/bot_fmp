from functions import *
from datetime import datetime

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
current_db = select("select name,username,chat_id from chats;")
for chat in current_db:
    print(prettyUsername(chat[0], chat[1]))
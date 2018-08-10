from functions import *

for chat in select(
        "select birthday,name,username from chats where status = 0 and substr(birthday,4,2) = '" + current_date('1')[
                                                                                                   3:] + "';"):
    print(chat[0])

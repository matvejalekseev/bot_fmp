from functions import *




chat_id = -241874218
chats = select("select chat_id from chats;")

for chat in chats:
    if chat_id in chat:
        print(chats)
    else:
        print('no')
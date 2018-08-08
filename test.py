from functions import *
from random import choice
from string import ascii_uppercase



def inchats(s):
    chats = select("select chat_id from chats where chat_id = " + str(s) + ";")
    if chats:
        return True
    else:
        return False

if inchats(-241874218):
    print('1')
else:
    print('0')
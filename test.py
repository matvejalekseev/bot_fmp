from functions import *
from random import choice
from string import ascii_uppercase



new_str = ''.join(choice(ascii_uppercase) for i in range(12))
print(new_str)
conn = sqlite3.connect("fmp_database.db")
cursor = conn.cursor()
cursor.execute("update invite set str = '" + new_str + "';")
conn.commit()
conn.close()

print(str(select("select str from invite;")))
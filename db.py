import sqlite3
from conf import db
 
conn = sqlite3.connect(db) # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
# Создание таблицы "Чаты"
#cursor.execute("DROP TABLE chats;")
#cursor.execute("CREATE TABLE chats(chat_id real, username text DEFAULT 'None', name text DEFAULT 'Your name', status INTEGER DEFAULT 0, UNIQUE(chat_id) );")
#моя личка chat_id = '109099327'
#тест = -241874218
#фмп = -310273520
#cursor.execute("insert into chats(status,chat_id) values (1,-310273520);")
#cursor.execute("ALTER TABLE chats add birthday text;")

# Создание таблицы "Статистики"
#cursor.execute("DROP TABLE stats;")
#cursor.execute("CREATE TABLE stats(stat text, number INTEGER DEFAULT 0, name text,  UNIQUE(stat) );")
#cursor.execute("INSERT INTO stats(stat,name) VALUES ('likes','Лайков');")
#cursor.execute("INSERT INTO stats(stat,name) VALUES ('dislikes','Дизлайков');")
#cursor.execute("INSERT INTO stats(stat,name) VALUES ('messages','Всего получено сообщений');")
#cursor.execute("INSERT INTO stats(stat,name) VALUES ('mass_messages','Всего отправлено сообщений в рассылках');")
#cursor.execute("INSERT INTO stats(stat,name) VALUES ('orders_send','Всего отправлено предзаказов');")


# Создание таблицы "Мероприятия"
#cursor.execute("DROP TABLE events;")
#cursor.execute("CREATE TABLE events(id integer primary key autoincrement, chat_id real, status INTEGER DEFAULT 0, "
#               "name text DEFAULT 'None', price text DEFAULT 'None', account text DEFAULT 'None');")

# Создание таблицы связи "Виновники меровприятий"
#cursor.execute("DROP TABLE u2e;")
#cursor.execute("CREATE TABLE u2e(event_id integer, chat_id real, UNIQUE(chat_id,event_id));")

# Создание таблицы "Статус текущего сбора"
#cursor.execute("DROP TABLE status_sbor;")
#10 - новый
#0 - не сдал
#1 - сдал, но не подтведил
#2 - сдал и подтвердил
#cursor.execute("CREATE TABLE status_sbor(chat_id real, status integer default 10, UNIQUE(chat_id));")

# Создание таблицы "Инвайт"
#cursor.execute("DROP TABLE invite;")
#cursor.execute("CREATE TABLE invite(str text);")
#cursor.execute("insert into invite(str) values ('hello');")

conn.commit()
conn.close()



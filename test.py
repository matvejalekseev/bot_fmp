import schedule
import time


url_3 = []
url = []
url.append('Портал БАРС Груп')
url.append('https://portal.bars-open.ru/')
url_3.append(url)
url = []
url.append('Confluence')
url.append('https://conf.bars-open.ru/')
url_3.append(url)
url = []
url.append('Jira')
url.append('http://jira.bars-open.ru/')
url_3.append(url)
url = []
url.append('Личный кабинет')
url.append('https://lk.bars-open.ru/user/login')
url_3.append(url)
url = []
url.append('Бронирование переговорных')
url.append('https://portal.bars-open.ru/services/index.php')
url_3.append(url)
url = []
url.append('Заказ техники')
url.append('https://portal.bars-open.ru/services/bp/121/list.php')
url_3.append(url)
url = []
url.append('Реестр бланков заявлений')
url.append('https://conf.bars-open.ru/pages/viewpage.action?pageId=16452933')
url_3.append(url)


for url in url_3:
    print(url[0] + url[1])

from functions import *




str_user = 'hello'
str_current = select("select str from invite limit 1;")[0]

if str_user in str_current:
    print('true')
else:
    print('no')
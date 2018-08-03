from functions \
    import *

for row in select("select name, number from stats;"):
    print(row[0], row[1])


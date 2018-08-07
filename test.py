import schedule
import time


from random import choice
from string import ascii_uppercase

new_str = ''.join(choice(ascii_uppercase) for i in range(12))
print(new_str)

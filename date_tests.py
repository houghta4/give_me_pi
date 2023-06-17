import datetime
from datetime import timedelta   
import time
swipe_in  = datetime.datetime.today()
new_swipe_in = (swipe_in - timedelta(minutes=5))
print(swipe_in,'\n', new_swipe_in)
print(swipe_in.minute, new_swipe_in.minute)


# t = time.ctime(time.time())
# start = t.index(":")
# end = t.rindex(":")
# print(f'minutes: {t[start:end]}')
# print(type(t), t)

START_TIME = time.ctime(time.time())
print(START_TIME)

PREV_MSG_SEND = START_TIME[START_TIME.index(':') + 1 : START_TIME.rindex(':')]

print('here:', PREV_MSG_SEND)
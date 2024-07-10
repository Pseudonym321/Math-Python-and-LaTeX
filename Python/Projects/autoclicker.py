import mouse
import time

'''
time.sleep(5)
position = mouse.get_position()
print(position)
'''

download = (671,111)
nextpage = (681,834)
emergency = (1776,659)

for i in range(10):
    position = mouse.get_position()
    mouse.drag(position[0], position[1], download[0], download[1],absolute=True, duration=0.1)
    time.sleep(1)
    mouse.click('left')
    time.sleep(3)
    position = mouse.get_position()
    mouse.drag(position[0], position[1], nextpage[0], nextpage[1],absolute=True, duration=0.1)
    time.sleep(3)
    mouse.click('left')
    time.sleep(1)
    position = mouse.get_position()
    mouse.drag(position[0], position[1], emergency[0], emergency[1],absolute=True, duration=0.1)
    time.sleep(2)

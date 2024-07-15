import mouse
import time

def find():
    time.sleep(5)
    position = mouse.get_position()
    print(position)


download = (671,111)
nextpage = (846, 485)
emergency = (1776,659)

def run():
    for i in range(10):
        position = mouse.get_position()
        mouse.drag(position[0], position[1], download[0], download[1],absolute=True, duration=0.1)
        time.sleep(1)
        mouse.click('left')
        position = mouse.get_position()
        mouse.drag(position[0], position[1], nextpage[0], nextpage[1],absolute=True, duration=0.1)
        time.sleep(1)
        mouse.click('left')
        position = mouse.get_position()
        mouse.drag(position[0], position[1], emergency[0], emergency[1],absolute=True, duration=0.1)
        time.sleep(1)

run()
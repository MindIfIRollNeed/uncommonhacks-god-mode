from leap_motion import *
import sys
import pygame
from pygame.locals import *
import Leap
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('172.16.7.165',10000)
print('starting up on {} port {}'.format(*server_address))


#class Hand:
#    def __init__(self):
#        self.visible = False
clock = pygame.time.Clock()
pygame.init()
screen1 = pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption('horizontal')

listener = SampleListener()
controller = Leap.Controller()
controller.add_listener(listener)

hand1 = Hand(screen1)
hand2 = Hand(screen1)


try:
    while True:

        dt = clock.tick(60)
        speed = float(dt)/64
        if controller.is_connected:
            frame = controller.frame()
            hands = frame.hands
            leaphand1 = hands[0]
            leaphand2 = hands[1]
            #print(frame)
            """
            if leaphand1.is_valid:
                print(str(leaphand1))
            if leaphand2.is_valid:
                print(str(leaphand2))
                """
            hand1.updatePos(leaphand1)
            hand2.updatePos(leaphand2)
            print("Hand1: " + str(hand1.coords))
            print("Hand2: " + str(hand2.coords))
            send_dict = json.dumps(
                {'hand1_x': (hand1.coords[0]-320)/64,
                'hand1_y': (hand1.coords[1]-240)/48,
                'hand1_valid': hand1.valid,
                'hand2_x': (hand2.coords[0]-320)/64,
                'hand2_y': (hand2.coords[1]-240)/48,
                'hand2_valid': hand2.valid
                })
            
            #send_data = str(hand1.coords) + ',' + str(hand2.coords)
            sock.sendto(send_dict.encode('UTF-8'),server_address)
        screen1.fill((0,0,0))
        hand1.draw()
        hand2.draw()
        pygame.display.update()
except KeyboardInterrupt:
    controller.remove_listener(listener)
    pass

import Leap
from math import *
import pygame


class Hand:
    def __init__(self, screen):
        self.offsetx = 320
        self.offsety = 240
        self.pos = [self.offsetx,self.offsety,0]
        self.ori = [0,0,0]
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(self.pos[0]-(self.width/2), self.pos[2]-(self.height/2), self.width, self.height)
        self.valid = False
        self.screen = screen
        self.coords = [0,0]

    def draw(self):
        if self.valid:
            pygame.draw.rect(self.screen, pygame.Color(255,255,255,20), self.rect)

    def updatePos(self, hand):
        self.pos = hand.palm_position
        self.valid = hand.is_valid
        self.coords = [self.offsetx + self.pos[0]-(self.width/2), self.offsety + self.pos[2]-(self.height/2)]
        self.rect = pygame.Rect(self.coords[0], self.coords[1], self.width, self.height)


class SampleListener(Leap.Listener):
    def on_init(self, controller):
        print("Leap initialized")
    def on_connect(self, controller):
        print("Leap connected")
    def on_disconnect(self, controller):
        print("Leap disconnected")
    def on_exit(self, controller):
        print("Leap exited")

    def on_frame(self, controller):
        global frame
        frame = controller.frame()
        if not frame.hands.is_empty:
            hands = frame.hands



import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import Leap
from math import *


"""
class Hand:
    def __init__(self):
        self.pos = [0,0,0]
        self.ori = [0,0,0]
        self.geom = pyglet.graphics.vertex_list(4, ('v2f', [-15,-10, 15,-10, 20,10, -20,10]))
        self.valid = False;
    def draw(self):
        glPushMatrix()
        glTranslatef(self.pos[0]+320,self.pos[1],0)
        glRotatef(self.ori[1],0,0,1)
        self.geom.draw(GL_QUADS)
        glPopMatrix()
"""

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
        global hand1, hand2, fingers1, fingers2

        frame = controller.frame()
        if not frame.hands.is_empty:

            leaphand1 = frame.hands[0]
            leaphand2 = frame.hands[1]

            #print('hand1: ' + str(frame.hands[0].is_valid))
            #print('hand2: ' + str(frame.hands[1].is_valid))

            leapfingers1 = leaphand1.fingers
            leapfingers2 = leaphand2.fingers

            for i in range(min(len(fingers1),len(leapfingers1))):
                fingers1[i].pos = leapfingers1[i].tip_position
            for i in range(min(len(fingers2),len(leapfingers2))):
                fingers2[i].pos = leapfingers2[i].tip_position

            normal1 = leaphand1.palm_normal
            direction1 = leaphand1.direction
            hand1.pos = leaphand1.palm_position
            hand1.ori = [ degrees(direction1.pitch), degrees(normal1.roll), degrees(direction1.yaw) ]
            hand1.valid = leaphand1.is_valid;

            normal2 = leaphand2.palm_normal
            direction2 = leaphand2.direction
            hand2.pos = leaphand2.palm_position
            hand2.ori = [ degrees(direction2.pitch), degrees(normal2.roll), degrees(direction2.yaw) ]
            hand2.valid = leaphand2.is_valid;
        else:
            hand1.valid = False;
            hand2.valid = False;


listener = SampleListener()
controller = Leap.Controller()
controller.add_listener(listener)



class Hand:
    def __init__(self):
        self.pos = [0,0,0]
        self.ori = [0,0,0]
        self.valid = False
        self.edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
        )
        self.vertices = (
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, -1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, -1, 1),
            (-1, 1, 1)
        )

    def draw(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()

hand1 = Hand()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    glRotate(45, 1, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                controller.remove_listener(listener)
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        hand1.draw()
        pygame.display.flip()
        pygame.time.wait(10)


main()


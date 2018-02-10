import pyglet
from pyglet.window import mouse
import random
import time 


class LeapEvent (object):

    def __init__ (self,name):
        self.name = name

class LeapMotionWidget (pyglet.event.EventDispatcher):
    
    def __init__ (self,controller):
        pyglet.event.EventDispatcher.__init__(self)
        self.controller = controller
    
    def leap_motion (self):
        event = LeapEvent('motion_event')
        self.dispatch_event("on_leap_motion",event)
        
    def on_leap_motion (self,event):
        print("default {}".format(event.name))        
        
LeapMotionWidget.register_event_type('on_leap_motion')

class MainWindow (pyglet.window.Window):

    def __init__ (self):
        pyglet.window.Window.__init__(self)
        self.label = pyglet.text.Label("hello kitty")
        pyglet.resource.path = ['./resources']
        self.image = pyglet.resource.image("kitty.jpg")

        self.prev_t = time.time()
        self.dt = 1
        self.image_loc = [0,0]
        self.default_cursor = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
        self.set_mouse_cursor(self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR))
        
        self.leap_motion_widget = LeapMotionWidget('da-controller')
        self.leap_motion_widget.push_handlers(self)
                
    def on_draw (self):
        self.clear()
        
        x,y = self.image_loc        
        #if time.time()-self.prev_t > self.dt:
        #self.prev_t = time.time()
        x = (x+random.randint(0,15)-6)%window.width
        y = (y+random.randint(0,25)-10)%window.height
        self.image_loc = [x,y]
    
        self.image.blit(x,y)
        self.label.draw()
    
    def on_mouse_motion (self,*args):
        self.leap_motion_widget.leap_motion()    
        
if __name__ == "__main__":
    window = MainWindow()
    pyglet.app.run()

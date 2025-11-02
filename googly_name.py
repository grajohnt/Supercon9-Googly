"""Template app for badge applications. Copy this file and update to implement your own app."""

import uasyncio as aio  # type: ignore

from apps.base_app import BaseApp
from net.net import register_receiver, send, BROADCAST_ADDRESS
from net.protocols import Protocol, NetworkFrame
from ui.page import Page
import ui.styles as styles
import lvgl
import random

"""
All protocols must be defined in their apps with unique ports. Ports must fit in uint8.
Try to pick a protocol ID that isn't in use yet; good luck.
Structdef is the struct library format string. This is a subset of cpython struct.
https://docs.micropython.org/en/latest/library/struct.html
"""
# NEW_PROTOCOL = Protocol(port=<PORT>, name="<NAME>", structdef="!")


class App(BaseApp):
    """Define a new app to run on the badge."""

    def __init__(self, name: str, badge):
        """ Define any attributes of the class in here, after super().__init__() is called.
            self.badge will be available in the rest of the class methods for accessing the badge hardware.
            If you don't have anything else to add, you can delete this method.
        """
        super().__init__(name, badge)
        # You can also set the sleep time when running in the foreground or background. Uncomment and update.
        # Remember to make background sleep longer so this app doesn't interrupt other processing.
        # self.foreground_sleep_ms = 10
        self.foreground_sleep_ms = 1000
        self.xo = random.randrange(-12,12)
        self.yo = random.randrange(-12,12)
        self.e1x = -100
        self.e1y = 0
        self.e1s = 90
        self.p1s = 50

        self.e2x = 0
        self.e2y = 0
        self.e2s = 90
        self.p2s = 50

        self.p1x = self.e1x + self.xo
        self.p1y = self.e1y + self.yo
        self.p2x = self.e2x + self.xo
        self.p2y = self.e2y + self.yo
        self.p1x_end = None
        self.p1y_end = None
        self.p2x_end = None
        self.p2y_end = None
      
        self.eye1 = None
        self.eye2 = None
        self.pup1 = None
        self.pup2 = None



    def start(self):
        """ Register the app with the system.
            This is where to register any functions to be called when a message of that protocol is received.
            The app will start running in the background.
            If you don't have anything else to add, you can delete this method.
        """
        super().start()
        # register_receiver(NEW_PROTOCOL, self.receive_message)

    def run_foreground(self):
        """ Run one pass of the app's behavior when it is in the foreground (has keyboard input and control of the screen).
            You do not need to loop here, and the app will sleep for at least self.foreground_sleep_ms milliseconds between calls.
            Don't block in this function, for it will block reading the radio and keyboard.
            If the app only runs in the background, you can delete this method.
        """

        #if self.badge.keyboard.f1():
        #    print("Hello ")
        #if self.badge.keyboard.f2():
        #    print("World.  ")
        #if self.badge.keyboard.f3():
        #    print("READ MORE ")
        #if self.badge.keyboard.f4():
        #    print("HACKADAY!")
        ## Co-op multitasking: all you have to do is get out
        if self.badge.keyboard.f5():
            self.badge.display.clear()
            self.switch_to_background()
 
        self.xo = random.randrange(-16,16)
        self.yo = random.randrange(-16,16)
        
        self.p1x_end = self.e1x + self.xo
        self.p1y_end = self.e1y + self.yo
        self.p2x_end = self.e2x + self.xo
        self.p2y_end = self.e2y + self.yo

        #self.p1x = self.e1x + self.xo
        #self.p1y = self.e1y + self.yo
        #self.p2x = self.e2x + self.xo
        #self.p2y = self.e2y + self.yo

        #Lets try to animate it
        anim_x = lvgl.anim_t()
        anim_x.init()
        anim_x.set_var(self.pup1)
        anim_x.set_values(self.p1x, self.p1x_end)
        anim_x.set_duration(1000)
        #anim_x.set_playback_duration(1000)
        #anim_x.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        anim_x.set_path_cb(lvgl.anim_t.path_ease_in_out)
        anim_x.set_custom_exec_cb(lambda a, v: self.pup1.set_x(v))
        anim_x.start()

        # --- Y animation ---
        anim_y = lvgl.anim_t()
        anim_y.init()
        anim_y.set_var(self.pup1)
        anim_y.set_values(self.p1y, self.p1y_end)
        anim_y.set_duration(1000)
        #anim_y.set_playback_duration(1000)
        #anim_y.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        anim_y.set_path_cb(lvgl.anim_t.path_ease_in_out)
        anim_y.set_custom_exec_cb(lambda a, v: self.pup1.set_y(v))
        anim_y.start()
        
        anim_x2 = lvgl.anim_t()
        anim_x2.init()
        anim_x2.set_var(self.pup2)
        anim_x2.set_values(self.p2x, self.p2x_end)
        anim_x2.set_duration(1000)
        #anim_x.set_playback_duration(1000)
        #anim_x.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        anim_x2.set_path_cb(lvgl.anim_t.path_ease_in_out)
        anim_x2.set_custom_exec_cb(lambda a, v: self.pup2.set_x(v))
        anim_x2.start()

        # --- Y animation ---
        anim_y2 = lvgl.anim_t()
        anim_y2.init()
        anim_y2.set_var(self.pup2)
        anim_y2.set_values(self.p2y, self.p2y_end)
        anim_y2.set_duration(1000)
        #anim_y.set_playback_duration(1000)
        #anim_y.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
        anim_y2.set_path_cb(lvgl.anim_t.path_ease_in_out)
        anim_y2.set_custom_exec_cb(lambda a, v: self.pup2.set_y(v))
        anim_y2.start()
        
       
        
        # End animation
        
        #Reset values
        self.p1x = self.p1x_end
        self.p1y = self.p1y_end
        self.p2x = self.p2x_end
        self.p2y = self.p2y_end
        
        #Uncomment to update without anmiation
        #self.pup1.align(lvgl.ALIGN.CENTER, self.p1x,self.p1y)
        #self.pup2.align(lvgl.ALIGN.CENTER,self.p2x,self.p2y)

        #self.pup1.align(lvgl.ALIGN.CENTER,p1x_end,p1y_end)


        #e1x = -100
        #e1y = 0
        #e1s = 90
        #p1s = 50

        #e2x = 0
        #e2y = 0
        #e2s = 90
        #p2s = 50

        #p1x = e1x + xo
        #p1y = e1y + yo
        #p2x = e2x + xo
        #p2y = e2y + yo


        

    def run_background(self):
        """ App behavior when running in the background.
            You do not need to loop here, and the app will sleep for at least self.background_sleep_ms milliseconds between calls.
            Don't block in this function, for it will block reading the radio and keyboard.
            If the app only does things when running in the foreground, you can delete this method.
        """
        super().run_background()

    def switch_to_foreground(self):
        """ Set the app as the active foreground app.
            This will be called by the Menu when the app is selected.
            Any one-time logic to run when the app comes to the foreground (such as setting up the screen) should go here.
            If you don't have special transition logic, you can delete this method.
        """
        super().switch_to_foreground()
        p = Page()
        ## Note this order is important: it renders top to bottom that the "content" section expands to fill empty space
        ## If you want to go fully clean-slate, you can draw straight onto the p.scr object, which should fit the full screen.
        #p.create_infobar(["My First App", "Prints to Serial Console"])
        p.create_content()
        #p.create_menubar(["Hello", "World", "Read more", "Hackaday", "Done"])
        #p.replace_screen()
        #circ.set_style_bg_color(lvgl.color_hex(0x0000000),0)
        
        #xo = random.randrange(-10,10)
        #yo = random.randrange(-10,10)
        
        #e1x = -100
        #e1y = 0
        #e1s = 90
        #p1x = e1x + xo
        #p1y = e1y + yo
        #p1s = 50

        #e2x = 0
        #e2y = 0
        #e2s = 90
        #p2x = e2x + xo
        #p2y = e2y + yo
        #p2s = 50


        self.eye1 = lvgl.obj(p.scr)
        self.eye1.set_size(self.e1s,self.e1s)
        self.eye1.align(lvgl.ALIGN.CENTER, self.e1x, self.e1y)
        self.eye1.set_style_radius(lvgl.RADIUS_CIRCLE, 0)
        self.eye1.set_style_bg_color(lvgl.color_white(),0)
        self.eye1.set_style_outline_width(1,0)
        self.eye1.set_style_outline_color(lvgl.color_black(),0)
        
        self.pup1 = lvgl.obj(p.scr)
        self.pup1.set_size(self.p1s,self.p1s)
        self.pup1.align(lvgl.ALIGN.CENTER, self.p1x,self.p1y)
        self.pup1.set_style_radius(lvgl.RADIUS_CIRCLE,0)
        self.pup1.set_style_bg_color(lvgl.color_black(),0)
        self.pup1.set_style_outline_color(lvgl.color_black(),0)

        self.eye2 = lvgl.obj(p.scr)
        self.eye2.set_size(self.e2s,self.e2s)
        self.eye2.align(lvgl.ALIGN.CENTER,self.e2x,self.e2y)
        self.eye2.set_style_radius(lvgl.RADIUS_CIRCLE, 0)
        self.eye2.set_style_bg_color(lvgl.color_white(),0)
        self.eye2.set_style_outline_width(1,0)
        self.eye2.set_style_outline_color(lvgl.color_black(),0)
        
        self.pup2 = lvgl.obj(p.scr)
        self.pup2.set_size(self.p2s,self.p2s)
        self.pup2.align(lvgl.ALIGN.CENTER,self.p2x,self.p2y)
        self.pup2.set_style_radius(lvgl.RADIUS_CIRCLE,0)
        self.pup2.set_style_bg_color(lvgl.color_black(),0)
        self.pup2.set_style_outline_color(lvgl.color_black(),0)
        
        
        p.replace_screen()

    def switch_to_background(self):
        """ Set the app as a background app.
            This will be called when the app is first started in the background and when it stops being in the foreground.
            If you don't have special transition logic, you can delete this method.
        """
        self.p = None
        super().switch_to_background()




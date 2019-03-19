#!/usr/bin/env python

import sys
sys.path.append('libs')

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from server import ViewerServer
from fogofwar import RevealRectangle
from manager import Manager
from getip import getIP

class MapScreen(Screen):
    pass

class ViewerApp(App):

    IPAddress = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ViewerApp, self).__init__(*args, **kwargs)
        self.server = ViewerServer(kivy_app=self)
        self.server.start()
        self.IPAddress = getIP()

    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)
        self.mapscreen = MapScreen(name='map')
        manager = Manager()
        manager.open(self.mapscreen)
        return manager

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27: # ESC
            return self.root.go_back()
        return False

    def on_pause(self):
        return True

    def reveal(self, d):
        self.mapscreen.ids.fog.set_json_areas(d)

if __name__ == '__main__':
    ViewerApp().run()

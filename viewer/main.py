#!/usr/bin/env python

import sys
sys.path.append('libs')

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from manager import Manager
from getip import getIP
from player_screen import PlayerScreen
import fogofwar


class ViewerApp(App):

    IPAddress = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ViewerApp, self).__init__(*args, **kwargs)
        self.IPAddress = getIP()

    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)
        self.player_screen = PlayerScreen(name='player')
        self.player_screen.start_server()
        manager = Manager()
        manager.open(self.player_screen)
        return manager

    def on_pause(self):
        return True

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27: # ESC
            return self.root.go_back()
        return False


if __name__ == '__main__':
    ViewerApp().run()

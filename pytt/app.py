#!/usr/bin/env python

import kivy
kivy.require('1.9.0')

import sys
from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from pytt.manager import Manager
from pytt.dmscreen import DMScreen
from pytt.player_screen import PlayerScreen
from pytt.getip import getIP

class MainMenuScreen(Screen):
    pass

def key(keycode, modifiers):
    if keycode > 255:
        return None # TODO
    ch = chr(keycode).upper()
    if modifiers:
        parts = sorted(modifiers)
        parts.append(ch)
        return '+'.join(parts)
    else:
        return ch

class PyTTApp(App):
    IPAddress = StringProperty(getIP())
    # this should belong to DMScreen, but I didn't manage to find a way to
    # make it working in the mess of kivy properties :(
    tool = StringProperty("move")

    def __init__(self, mapfile, server, **kwargs):
        super(PyTTApp, self).__init__(**kwargs)
        self.default_mapfile = mapfile
        self.default_server = server
        self.dmscreen = None
        self.player_screen = None

    def build(self):
        if platform != 'android':
            # it seems that on android touch events also send a <space> key
            # event, no idea why. Too bad, we don't really need keyboard
            # shortcuts on android anyway, just disable them
            Window.bind(on_keyboard=self.on_keyboard)
        self.manager = Manager()
        if self.default_mapfile:
            # we passed a mapfile from the command line: start directly the DM screen
            self.open_dmscreen()
        else:
            # no cmdline argument, open the menu
            self.manager.open(MainMenuScreen())
        return self.manager

    def on_pause(self):
        return True

    def on_keyboard(self, window, keycode, scancode, text, modifiers):
        if keycode == 27: # ESC
            return self.root.go_back()
        k = key(keycode, modifiers)
        self.root.on_key_press(self, k)

    def on_tool(self, _, tool):
        if self.dmscreen:
            self.dmscreen.select_tool(tool)

    def open_dmscreen(self):
        if self.dmscreen is None:
            self.dmscreen = DMScreen(name='dm',
                                     mapfile=self.default_mapfile,
                                     server=self.default_server)
        self.manager.open(self.dmscreen)

    def open_playerscreen(self):
        if self.player_screen is None:
            self.player_screen = PlayerScreen()
            self.player_screen.start_server()
        self.manager.open(self.player_screen)


def main():
    mapfile = ''
    server = '127.0.0.1'
    n = len(sys.argv)
    if n == 2:
        mapfile = sys.argv[1]
    elif n == 3:
        mapfile = sys.argv[1]
        server = sys.argv[2]
    PyTTApp(mapfile=mapfile, server=server).run()

#!/usr/bin/env python

import kivy
kivy.require('1.9.0')

import sys
from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from pytt.manager import Manager
from pytt.dmscreen import DMScreen

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

class DMApp(App):
    mapfile = StringProperty('')
    server = StringProperty('127.0.0.1')

    # this should belong to DMScreen, but I didn't manage to find a way to
    # make it working in the mess of kivy properties :(
    tool = StringProperty("move")

    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)
        self.dmscreen = DMScreen(name='dm', mapfile=self.mapfile, server=self.server)
        manager = Manager()
        manager.open(self.dmscreen)
        return manager

    def on_pause(self):
        return True

    def on_keyboard(self, window, keycode, scancode, text, modifiers):
        if keycode == 27: # ESC
            return self.root.go_back()
        #
        k = key(keycode, modifiers)
        self.root.on_key_press(self, k)

    def on_tool(self, _, tool):
        if self.dmscreen:
            self.dmscreen.select_tool(tool)


def main():
    n = len(sys.argv)
    if n == 2:
        mapfile = sys.argv[1]
        server = '127.0.0.1'
    elif n == 3:
        mapfile = sys.argv[1]
        server = sys.argv[2]
    else:
        print 'Usage: dm.py MAPFILE [SERVER]'
        sys.exit(1)
    DMApp(mapfile=mapfile, server=server).run()

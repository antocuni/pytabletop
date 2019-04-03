#!/usr/bin/env python

import kivy
kivy.require('1.9.0')

import sys
from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from fogofwar import RevealRectangle
from tools import Tool, RectangleTool


class DMApp(App):
    mapfile = StringProperty('')
    server = StringProperty('127.0.0.1')
    tool = StringProperty("move")

    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)

    def reveal_url(self):
        return 'http://%s:5000/reveal/' % (self.server)

    def on_pause(self):
        return True

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        print 'got key', key

    @property
    def fog(self):
        return self.root.ids.fog

    def do_sync(self):
        import requests
        areas = self.fog.get_json_areas()
        resp = requests.post(self.reveal_url(), json=areas)
        print resp
        print resp.text

    def on_tool(self, _, tool):
        self.fog.locked = (tool != 'move')
        if tool == 'move':
            self.fog.tool = Tool()
        elif tool == 'rect':
            self.fog.tool = RectangleTool()
        else:
            print 'Unknown tool: %s' % tool

    def adjust_rotation(self):
        rot = self.fog.rotation
        if rot % 90 != 0:
            self.fog.rotation = int(rot % 90) * 90
        self.fog.rotation += 90


if __name__ == '__main__':
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

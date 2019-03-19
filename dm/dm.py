#!/usr/bin/env python

import kivy
kivy.require('1.9.0')

import sys
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.togglebutton import ToggleButton
from fogofwar import RevealRectangle
from tools import Tool, RectangleTool


class DMApp(App):
    server = StringProperty('127.0.0.1')
    tool = StringProperty("move")

    def reveal_url(self):
        return 'http://%s:5000/reveal/' % (self.server)

    def on_pause(self):
        return True

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
    server = '127.0.0.1'
    if len(sys.argv) >= 2:
        server = sys.argv[1]
    DMApp(server=server).run()

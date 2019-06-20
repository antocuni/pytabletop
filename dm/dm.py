#!/usr/bin/env python

import kivy
kivy.require('1.9.0')

import sys
from urlparse import urljoin
from kivy.app import App
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from fogofwar import RevealRectangle
from tools import Tool, RectangleTool
from manager import Manager
from pasteimage import PasteImageScreen, get_png_from_clipboard

class DMScreen(Screen):
    mapfile = StringProperty('')
    server = StringProperty('127.0.0.1')
    port = StringProperty('5000')

    @property
    def fog(self):
        return self.ids.fog

    def url(self, path):
        base = 'http://%s:%s' % (self.server, self.port)
        return urljoin(base, path)

    def cmd_send_map(self):
        import requests
        with open(self.mapfile, 'rb') as f:
            url = self.url('/load_map/')
            resp = requests.post(url, files={'image': f})
            print resp
            print resp.text

    def cmd_sync(self):
        import requests
        areas = self.fog.get_json_areas()
        resp = requests.post(self.url('/reveal/'), json=areas)
        print resp
        print resp.text

    def cmd_adjust_rotation(self):
        rot = self.fog.rotation
        if rot % 90 != 0:
            self.fog.rotation = int(rot % 90) * 90
        self.fog.rotation += 90

    def send_image(self, stream):
        import requests
        url = self.url('/show_image/')
        resp = requests.post(url, files={'image': stream})
        print resp
        print resp.text


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
    tool = StringProperty("move")

    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)
        self.dmscreen = DMScreen(name='dm', mapfile=self.mapfile,
                                 server=self.server)
        manager = Manager()
        manager.open(self.dmscreen)
        return manager

    def on_pause(self):
        return True

    # kill this eventually
    @property
    def fog(self):
        return self.dmscreen.ids.fog

    def on_keyboard(self, window, keycode, scancode, text, modifiers):
        if keycode == 27: # ESC
            return self.root.go_back()
        #
        k = key(keycode, modifiers)
        if k == ' ':
            self.tool = 'move'
        elif k == 'R':
            self.tool = 'rect'
        elif k == 'ctrl+S':
            # sync
            self.do_sync()
        elif k == 'ctrl+V':
            png_data = get_png_from_clipboard()
            if png_data is None:
                print 'No image in the clipboard'
            else:
                screen = PasteImageScreen(name="paste", png_data=png_data)
                self.root.open(screen)

    def on_tool(self, _, tool):
        self.fog.locked = (tool != 'move')
        if tool == 'move':
            self.fog.tool = Tool()
        elif tool == 'rect':
            self.fog.tool = RectangleTool()
        else:
            print 'Unknown tool: %s' % tool




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

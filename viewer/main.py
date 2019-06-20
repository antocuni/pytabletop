#!/usr/bin/env python

import sys
sys.path.append('libs')

import kivy
kivy.require('1.9.0')

import io
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from server import ViewerServer
from fogofwar import RevealRectangle
from manager import Manager
from getip import getIP

class PlayerScreen(Screen):
    map_texture = ObjectProperty(None)

class ImageScreen(Screen):
    image_texture = ObjectProperty(None)


class ViewerApp(App):

    IPAddress = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ViewerApp, self).__init__(*args, **kwargs)
        self.server = ViewerServer(kivy_app=self)
        self.server.start()
        self.IPAddress = getIP()

    def build(self):
        Window.bind(on_keyboard=self.on_keyboard)
        self.playerscreen = PlayerScreen(name='player')
        manager = Manager()
        manager.open(self.playerscreen)
        return manager

    def on_pause(self):
        return True

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27: # ESC
            return self.root.go_back()
        return False

    def reveal(self, d):
        self.playerscreen.ids.fog.set_json_areas(d)

    def load_map(self, data):
        stream = io.BytesIO(data)
        img = CoreImage(stream, ext="png")
        self.playerscreen.map_texture = img.texture

    def show_image(self, data):
        stream = io.BytesIO(data)
        img = CoreImage(stream, ext="png")
        self.root.open(ImageScreen(image_texture=img.texture, name='img'))

if __name__ == '__main__':
    ViewerApp().run()

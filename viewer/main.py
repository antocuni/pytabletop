#!/usr/bin/env python

import sys
sys.path.append('libs')

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.properties import StringProperty
from server import ViewerServer
from fogofwar import RevealRectangle
from getip import getIP

class ViewerApp(App):

    IPAddress = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ViewerApp, self).__init__(*args, **kwargs)
        self.server = ViewerServer(kivy_app=self)
        self.server.start()
        self.IPAddress = getIP()

    def on_pause(self):
        return True

    def reveal(self, d):
        self.root.ids.fog.set_json_areas(d)

if __name__ == '__main__':
    ViewerApp().run()

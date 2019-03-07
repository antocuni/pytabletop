#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

from kivy.app import App
from server import ViewerServer
from fogofwar import RevealRectangle


class ViewerApp(App):

    def __init__(self, *args, **kwargs):
        super(ViewerApp, self).__init__(*args, **kwargs)
        self.server = ViewerServer(kivy_app=self)
        self.server.start()

    def on_pause(self):
        return True

    def reveal(self, d):
        self.root.ids.fog.set_json_areas(d)

if __name__ == '__main__':
    ViewerApp().run()

#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

from kivy.app import App
from server import ViewerServer
from fogofwar import RevealRectangle


class Viewer(App):

    def __init__(self, *args, **kwargs):
        super(Viewer, self).__init__(*args, **kwargs)
        self.server = ViewerServer(kivy_app=self)
        self.server.start()

    def on_pause(self):
        return True

    def reveal(self, d):
        fog = self.root.ids.fog
        fog.clear()
        for rect in d['areas']:
            assert rect['type'] == 'rectangle'
            r = RevealRectangle(pos=rect['pos'], size=rect['size'])
            fog.add_widget(r)

if __name__ == '__main__':
    Viewer().run()

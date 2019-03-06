#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

from kivy.app import App
from fogofwar import RevealRectangle


class PyTableTopApp(App):

    REVEAL_URL = 'http://127.0.0.1:5000/reveal/'

    def on_pause(self):
        return True

    def do_sync(self):
        import requests
        fog = self.root.ids.fog
        areas = fog.get_json_areas()
        resp = requests.post(self.REVEAL_URL, json=areas)
        print resp
        print resp.text

if __name__ == '__main__':
    PyTableTopApp().run()

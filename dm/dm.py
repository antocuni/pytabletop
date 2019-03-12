#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

import sys
from kivy.app import App
from kivy.properties import StringProperty
from fogofwar import RevealRectangle


class DMApp(App):
    server = StringProperty('127.0.0.1')

    def reveal_url(self):
        return 'http://%s:5000/reveal/' % (self.server)

    def on_pause(self):
        return True

    def do_sync(self):
        import requests
        fog = self.root.ids.fog
        areas = fog.get_json_areas()
        resp = requests.post(self.reveal_url(), json=areas)
        print resp
        print resp.text


if __name__ == '__main__':
    server = '127.0.0.1'
    if len(sys.argv) >= 2:
        server = sys.argv[1]
    DMApp(server=server).run()

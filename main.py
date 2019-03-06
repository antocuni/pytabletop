#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

from kivy.app import App
from fogofwar import RevealRectangle


class PyTableTopApp(App):

    def on_pause(self):
        return True

    def do_sync(self):
        fog = self.root.ids.fog
        fog2 = self.root.ids.fog2

        # remove all the RevealRectangle from fog2
        for w in fog2.children[:]:
            if isinstance(w, RevealRectangle):
                fog2.remove_widget(w)
        
        # readd new children
        for rect in fog.children:
            if isinstance(rect, RevealRectangle):
                newrect = RevealRectangle(pos=rect.pos, size=rect.size)
                fog2.add_widget(newrect)

if __name__ == '__main__':
    PyTableTopApp().run()

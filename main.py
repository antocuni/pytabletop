#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import DragBehavior


class FogOfWar(RelativeLayout):
    source = ObjectProperty()

class RevealRectangle(DragBehavior, Widget):
    texture = ObjectProperty(None, allownone=True)

    def _update_texture(self, instance, value):
        if not self.parent:
            #print 'no parent'
            return
        map_texture = self.parent.ids.map.texture
        if not map_texture:
            #print 'no texture'
            return
        self.texture = map_texture.get_region(self.x, self.y,
                                              self.width, self.height)

    on_pos = _update_texture
    on_size = _update_texture
    on_parent = _update_texture


class PyTableTopApp(App):

    def on_pause(self):
        return True

    def do_reveal(self):
        fog = self.root.ids.fog
        newrect = RevealRectangle(pos=(50, 400), size=(250, 250))
        fog.add_widget(newrect)

    def do_clear(self):
        pass
        #self.root.ids.map.visible_areas[:] = []

if __name__ == '__main__':
    PyTableTopApp().run()

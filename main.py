#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.graphics import (Rectangle, Color, StencilPop, StencilPush,
                           StencilUse, StencilUnUse, PushMatrix, PopMatrix,
                           Translate)


class FogOfWar(Image):
    visible_areas = ListProperty()

    ## def __init__(self, *args, **kwargs):
    ##     super(FogOfWar, self).__init__(*args, **kwargs)
    ##     #self.redraw()

    def on_pos(self, instance, value):
        self.redraw()

    def on_size(self, instance, value):
        self.redraw()

    def on_visible_areas(self, instance, value):
        self.redraw()

    def redraw(self):
        self.canvas.after.clear()
        with self.canvas.after:
            PushMatrix()
            Translate(*self.pos)

            StencilPush()
            for myrect in self.visible_areas:
                Rectangle(pos=myrect.pos, size=myrect.size)

            StencilUse(op="greater")
            # this is the shadow which hides the whole map
            Color(0, 0, 0, 0.7)
            Rectangle(pos=(0, 0), size=self.size)

            StencilUnUse()
            for myrect in self.visible_areas:
                Rectangle(pos=myrect.pos, size=myrect.size)

            StencilPop()
            PopMatrix()


class PyTableTopApp(App):

    def on_pause(self):
        return True

    def do_reveal(self):
        mymap = self.root.ids.map
        r1 = Rectangle(pos=(500, 500), size=(200, 200))
        r2 = Rectangle(pos=(400, 400), size=(200, 200))
        mymap.visible_areas.append(r1)
        mymap.visible_areas.append(r2)

    def do_clear(self):
        self.root.ids.map.visible_areas[:] = []

if __name__ == '__main__':
    PyTableTopApp().run()

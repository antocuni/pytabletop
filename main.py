#!/usr/bin/env python

import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import DragBehavior

def bounding_rect(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    pos = x1, y1
    size = (x2-x1, y2-y1)
    return pos, size

class FogOfWar(RelativeLayout):
    source = ObjectProperty()
    scale = NumericProperty(1.0)

    def to_local(self, x, y, **k):
        xx = (x - self.x) / self.scale
        yy = (y - self.y) / self.scale
        return xx, yy

    current_rect = None
    current_origin = None
    def on_map_touch_down(self, touch):
        if touch.button == 'left':
            self.current_origin = touch.pos
            self.current_rect = RevealRectangle(pos=touch.pos, size=(1, 1))
            self.add_widget(self.current_rect)
            touch.grab(self.ids.map)
        elif touch.button == 'scrolldown':
            self.scale = max(0.1, self.scale - 0.1)
        elif touch.button == 'scrollup':
            self.scale += 0.1

    def on_map_touch_move(self, touch):
        if touch.button == 'left':
            pos, size = bounding_rect(self.current_origin, touch.pos)
            self.current_rect.pos = pos
            self.current_rect.size = size

    def on_map_touch_up(self, touch):
        if touch.button == 'left':
            if (self.current_rect and
                self.current_rect.width < 5 and
                self.current_rect.height < 5):
                # too small, remove it!
                self.remove_widget(self.current_rect)
                self.current_rect = None
                self.current_origin = None


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

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                self.parent.remove_widget(self)
            super(RevealRectangle, self).on_touch_down(touch)
            return True


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

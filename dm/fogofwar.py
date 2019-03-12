import kivy
kivy.require('1.0.6')

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.behaviors import DragBehavior

Builder.load_string("""
<FogOfWar>:
    ## canvas.after:
    ##     Color:
    ##         rgba: 1, 0, 1, 1
    ##     Line:
    ##         rectangle: self.x,self.y,self.width,self.height
    ##         dash_offset: 5
    ##         dash_length: 3

    do_rotation: False
    do_translation: False
    do_scale: False

    Image:
        id: map
        source: root.source
        pos: 0, 0
        size: self.texture.size if self.texture else (100, 100)
        size_hint: None, None

        on_touch_down: root.on_map_touch_down(args[1])
        on_touch_move: root.on_map_touch_move(args[1])
        on_touch_up: root.on_map_touch_up(args[1])

        canvas.after:
            Color:
                rgba: (0, 0, 0, 0.8) if root.dm else (0, 0, 0, 1)
            Rectangle:
                pos: self.pos
                size: self.size


<RevealRectangle>:
    drag_distance: 0
    drag_rect_x: self.x
    drag_rect_y: self.y

    # enable dragging only for dm
    drag_rect_width: self.width if self.dm else 0
    drag_rect_height: self.height if self.dm else 0
    drag_timeout: 10000000 if self.dm else 0

    size_hint: None, None

    canvas.after:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            texture: self.texture
            size: self.size
            pos: self.pos

        ## Color:
        ##     rgba: 1, 0, 0, 1
        ## Line:
        ##     rectangle: self.x,self.y,self.width,self.height
        ##     dash_offset: 5
        ##     dash_length: 3


# <RevealEllipse>:
#     drag_rectangle: self.x, self.y, self.width, self.height
#     drag_timeout: 10000000
#     drag_distance: 0
#     size_hint: None, None

#     canvas.after:
#         Color:
#             rgba: 1, 1, 1, 1
#         Ellipse:
#             pos: self.pos
#             size: self.size
#             texture: self.texture


""")


def bounding_rect(pos1, pos2):
    if pos1 is None or pos2 is None:
        # temporary workaround
        print 'wrong position :(', pos1, pos2
        return (0, 0), (1, 1)
    x1, y1 = pos1
    x2, y2 = pos2
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    pos = x1, y1
    size = (x2-x1, y2-y1)
    return pos, size

class FogOfWar(ScatterLayout):
    dm = BooleanProperty(False)
    source = ObjectProperty()

    def clear(self):
        # remove all the revealed areas
        for w in self.content.children[:]:
            if isinstance(w, RevealRectangle):
                self.remove_widget(w)

    def get_json_areas(self):
        areas = []
        for rect in self.content.children:
            if isinstance(rect, RevealRectangle):
                areas.append({
                    'type': 'rectangle',
                    'pos': rect.pos,
                    'size': rect.size
                    })
        return {'areas': areas}

    def set_json_areas(self, d):
        self.clear()
        for rect in d['areas']:
            assert rect['type'] == 'rectangle'
            r = RevealRectangle(pos=rect['pos'], size=rect['size'],
                                dm=self.dm, fog=self)
            self.add_widget(r)

    def get_button(self, touch):
        # on Android we don't have buttons, we assume it's left, i.e. the
        # default
        return getattr(touch, 'button', 'left')

    current_rect = None
    current_origin = None
    def on_map_touch_down(self, touch):
        if not self.dm or not self.collide_point(*touch.pos):
            return
        button = self.get_button(touch)
        if button == 'left':
            self.current_origin = touch.pos
            self.current_rect = RevealRectangle(pos=touch.pos, size=(1, 1),
                                                dm=self.dm, fog=self)
            self.add_widget(self.current_rect)
            touch.grab(self.ids.map)

    def on_map_touch_move(self, touch):
        if not self.dm: #or not self.collide_point(*touch.pos):
            return
        if self.get_button(touch) == 'left':
            pos, size = bounding_rect(self.current_origin, touch.pos)
            self.current_rect.pos = pos
            self.current_rect.size = size
            return True

    def on_map_touch_up(self, touch):
        if not self.dm: #or not self.collide_point(*touch.pos):
            return
        if self.get_button(touch) == 'left':
            if (self.current_rect and
                self.current_rect.width < 5 and
                self.current_rect.height < 5):
                # too small, remove it!
                self.remove_widget(self.current_rect)
            self.current_rect = None
            self.current_origin = None


class RevealRectangle(DragBehavior, Widget):
    dm = BooleanProperty(False)
    texture = ObjectProperty(None, allownone=True)
    fog = ObjectProperty(None)

    def _update_texture(self, instance, value):
        if not self.fog:
            return
        map_texture = self.fog.ids.map.texture
        if not map_texture:
            return
        self.texture = map_texture.get_region(self.x, self.y,
                                              self.width, self.height)

    on_pos = _update_texture
    on_size = _update_texture
    on_parent = _update_texture

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.dm and touch.is_double_tap:
                self.parent.remove_widget(self)
                return True
            else:
                return super(RevealRectangle, self).on_touch_down(touch)

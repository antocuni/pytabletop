from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.behaviors import DragBehavior

Builder.load_string("""
<FogOfWar>:
    locked: False
    do_rotation: not self.locked
    do_translation: not self.locked
    do_scale: not self.locked
    auto_bring_to_front: False

    Image:
        id: map
        source: root.source
        pos: 0, 0
        size: self.texture.size if self.texture else (100, 100)
        size_hint: None, None

        on_touch_down: root.tool.on_touch_down(root, args[1])
        on_touch_move: root.tool.on_touch_move(root, args[1])
        on_touch_up: root.tool.on_touch_up(root, args[1])

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

class Tool(EventDispatcher):
    """
    Abstract class for a generic tool which can do interactive actions on the
    FogOfWar
    """

    def on_touch_down(self, fog, touch):
        pass

    def on_touch_move(self, fog, touch):
        pass

    def on_touch_up(self, fog, touch):
        pass

class MyScatterPlaneLayout(ScatterLayout):
    # the ScatterPlaneLayout which is distributed with kivy 1.9.1 seems buggy:
    # it inherits from ScatterPlane instead of ScatterLayout. This is
    # supposedly the correct version
    def collide_point(self, x, y):
        return True


class FogOfWar(MyScatterPlaneLayout):
    dm = BooleanProperty(False)
    source = ObjectProperty()
    tool = ObjectProperty(Tool())

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

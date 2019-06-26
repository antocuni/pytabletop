from kivy.event import EventDispatcher
from pytt.fogofwar import Tool, RevealRectangle

def bounding_rect(pos1, pos2):
    if pos1 is None or pos2 is None:
        # this should never happen, but better to return a dummy value than to
        # crash
        print 'wrong position :(', pos1, pos2
        return (0, 0), (1, 1)
    x1, y1 = pos1
    x2, y2 = pos2
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])
    pos = x1, y1
    size = (x2-x1, y2-y1)
    return pos, size


class RectangleTool(Tool):
    """
    Interactively reveal a rectangle of the map
    """
    rect = None
    origin = None

    def get_button(self, touch):
        # on Android we don't have buttons, we assume it's left, i.e. the
        # default
        return getattr(touch, 'button', 'left')

    def on_touch_down(self, fog, touch):
        if not fog.collide_point(*touch.pos) or self.get_button(touch) != 'left':
            return
        self.origin = touch.pos
        self.rect = RevealRectangle(pos=touch.pos, size=(1, 1),
                                    dm=fog.dm, fog=fog)
        fog.add_widget(self.rect)
        touch.grab(fog.ids.map)

    def on_touch_move(self, fog, touch):
        if (self.rect is None or self.origin is None or
            self.get_button(touch) != 'left'):
            return
        pos, size = bounding_rect(self.origin, touch.pos)
        self.rect.pos = pos
        self.rect.size = size

    def on_touch_up(self, fog, touch):
        if (self.rect is None or self.origin is None or
            self.get_button(touch) != 'left'):
            return
        if (self.rect and
            self.rect.width < 5 and
            self.rect.height < 5):
            # too small, remove it!
            fog.remove_widget(self.rect)
        self.rect = None
        self.origin = None

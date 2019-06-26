import io
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty, ObjectProperty
from pytt.player_server import PlayerServer

class ShowImageScreen(Screen):
    image_texture = ObjectProperty(None)


class PlayerScreen(Screen):
    map_texture = ObjectProperty(None)
    server = ObjectProperty()

    def start_server(self):
        self.server = PlayerServer(player_screen=self)
        self.server.start()

    def reveal(self, d):
        self.ids.fog.set_json_areas(d)

    def load_map(self, data):
        stream = io.BytesIO(data)
        img = CoreImage(stream, ext="png")
        self.map_texture = img.texture

    def show_image(self, data):
        stream = io.BytesIO(data)
        img = CoreImage(stream, ext="png")
        self.manager.open(ShowImageScreen(image_texture=img.texture, name='img'))


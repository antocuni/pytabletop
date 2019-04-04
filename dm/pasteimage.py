import io
from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

class Clipboard(object):
    _scrap = None

    @property
    def scrap(self):
        if self._scrap is None:
            import pygame.scrap
            pygame.scrap.init()
            self._scrap = pygame.scrap
        return self._scrap

    def get_png(self):
        data = self.scrap.get('image/png')
        if data == '':
            return None
        ## with open('paste.png', 'wb') as f:
        ##     f.write(data)
        return data

CLIPBOARD = Clipboard()


class PasteImageScreen(Screen):
    png_data = ObjectProperty(None)
    texture = ObjectProperty(None)

    def on_png_data(self, instance, value):
        if self.png_data is not None:
            stream = io.BytesIO(self.png_data)
            img = CoreImage(stream, ext="png")
            self.texture = img.texture

    def do_send(self, app):
        stream = io.BytesIO(self.png_data)
        app.send_image(stream)
        app.root.go_back()

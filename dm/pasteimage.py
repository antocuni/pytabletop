import io
import subprocess
import errno
from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

def get_png_from_clipboard():
    cmd = ['xxxclip', '-o', '-selection', 'clipboard', '-t', 'image/png']
    try:
        return subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        # most likely it means that we don't have an image in the clipboard
        return None
    except OSError as e:
        if e.errno == errno.ENOENT:
            print 'xclip: %s' % (e.strerror,)
            return None
        raise

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

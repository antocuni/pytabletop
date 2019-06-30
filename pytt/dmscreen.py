from urlparse import urljoin
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from pytt.tools import Tool, RectangleTool
from pytt.pasteimage import PasteImageScreen, get_png_from_clipboard

class DMScreen(Screen):
    mapfile = StringProperty('')
    server = StringProperty('127.0.0.1')
    port = StringProperty('5000')

    @property
    def fog(self):
        return self.ids.fog

    def url(self, path):
        base = 'http://%s:%s' % (self.server, self.port)
        return urljoin(base, path)

    def on_key_press(self, app, k):
        if k == ' ':
            app.tool = 'move'
        elif k == 'R':
            app.tool = 'rect'
        elif k == 'ctrl+S':
            # sync
            self.cmd_sync()
        elif k == 'ctrl+V':
            png_data = get_png_from_clipboard()
            if png_data is None:
                print 'No image in the clipboard'
            else:
                screen = PasteImageScreen(name="paste",
                                          dm=self,
                                          png_data=png_data)
                app.root.open(screen)

    def select_tool(self, tool):
        self.fog.locked = (tool != 'move')
        if tool == 'move':
            self.fog.tool = Tool()
        elif tool == 'rect':
            self.fog.tool = RectangleTool()
        else:
            print 'Unknown tool: %s' % tool

    def cmd_load_map(self):
        from kivy.utils import platform
        if platform == 'android':
            from pytt.select_image import user_select_image
            user_select_image(self.on_image_selected)
        else:
            print 'TODO: implement load_map on desktops'

    def on_image_selected(self, filename):
        self.mapfile = filename

    def cmd_send_map(self):
        import requests
        with open(self.mapfile, 'rb') as f:
            url = self.url('/load_map/')
            resp = requests.post(url, files={'image': f})
            print resp
            print resp.text

    def cmd_sync(self):
        import requests
        areas = self.fog.get_json_areas()
        resp = requests.post(self.url('/reveal/'), json=areas)
        print resp
        print resp.text

    def cmd_adjust_rotation(self):
        rot = self.fog.rotation
        if rot % 90 != 0:
            self.fog.rotation = int(rot % 90) * 90
        self.fog.rotation += 90

    def send_image(self, stream):
        import requests
        url = self.url('/show_image/')
        resp = requests.post(url, files={'image': stream})
        print resp
        print resp.text


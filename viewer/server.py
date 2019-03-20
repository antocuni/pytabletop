import threading
from kivy.clock import mainthread
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
import flask
from flask import current_app

tabletop = flask.Blueprint('tabletop', __name__)

def error(message, status=403):
    myjson = flask.jsonify(result='error',
                           message=message)
    return myjson, status

@mainthread
def call_mainthread(fn, *args, **kwargs):
    return fn(*args, **kwargs)


@tabletop.route('/')
def index():
    current_app.server.count += 1
    return 'Count: %d' % current_app.server.count

@tabletop.route('/reveal/', methods=['POST'])
def reveal():
    reveal_dict = flask.request.json
    if reveal_dict is None:
        return error('Expected JSON request', 400)
    #
    current_app.logger.info('\nReveal: %s' % reveal_dict)
    current_app.server.kivy_app.reveal(reveal_dict)
    return flask.jsonify(result='OK')

@tabletop.route('/show_image/', methods=['GET', 'POST'])
def show_image():
    request = flask.request
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            return error("no image part")
        image = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if image.filename == '':
            return error("empty file")

        if file:
            image_data = image.stream.read()
            call_mainthread(current_app.server.kivy_app.show_image,
                            image_data)
            return flask.jsonify(result='OK')
    return '''
    <!doctype html>
    <title>Show Image</title>
    <h1>Show Image</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

###########################################

class ViewerServer(EventDispatcher):
    thread = None
    map_name = StringProperty()
    count = NumericProperty(0)
    kivy_app = ObjectProperty()

    def create_app(self):
        self.app = flask.Flask('tabletop_viewer')
        self.app.register_blueprint(tabletop)
        self.app.server = self
        return self.app

    def _run(self):
        import logging
        app = self.create_app()
        logging.basicConfig()
        logging.getLogger('werkzeug').setLevel(logging.INFO)
        app.run(host='0.0.0.0', debug=False)

    def start(self):
        self.thread = threading.Thread(target=self._run, name='ViewerServer')
        self.thread.daemon = True
        self.thread.start()


if __name__ == '__main__':
    serv = ViewerServer()
    serv._run()


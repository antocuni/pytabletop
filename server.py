import threading
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
import flask
from flask import current_app

tabletop = flask.Blueprint('tabletop', __name__)
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


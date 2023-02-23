# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import errno
import logging
import socket
import sys
import time
from threading import Thread

import requests
from flask import Flask, g
from werkzeug.serving import make_server

from ..utils.json import InkStitchJSONProvider
from .install import install
from .simulator import simulator
from .stitch_plan import stitch_plan
from .preferences import preferences


class APIServer(Thread):
    def __init__(self, *args, **kwargs):
        self.extension = args[0]
        Thread.__init__(self, *args[1:], **kwargs)
        self.daemon = True
        self.app = None
        self.host = None
        self.port = None
        self.ready = False

        self.__setup_app()
        self.flask_server = None
        self.server_thread = None

    def __setup_app(self):  # noqa: C901
        # Disable warning about using a development server in a production environment
        cli = sys.modules['flask.cli']
        cli.show_server_banner = lambda *x: None

        self.app = Flask(__name__)
        self.app.json = InkStitchJSONProvider(self.app)

        self.app.register_blueprint(simulator, url_prefix="/simulator")
        self.app.register_blueprint(stitch_plan, url_prefix="/stitch_plan")
        self.app.register_blueprint(install, url_prefix="/install")
        self.app.register_blueprint(preferences, url_prefix="/preferences")

        @self.app.before_request
        def store_extension():
            # make the InkstitchExtension object available to the view handling
            # this request
            g.extension = self.extension

        @self.app.route('/ping')
        def ping():
            return "pong"

    def stop(self):
        self.flask_server.shutdown()
        self.server_thread.join()

    def disable_logging(self):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    def run(self):
        self.disable_logging()

        self.host = "127.0.0.1"
        self.port = 5000

        while True:
            try:
                self.flask_server = make_server(self.host, self.port, self.app)
                self.server_thread = Thread(target=self.flask_server.serve_forever)
                self.server_thread.start()
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    self.port += 1
                    continue
                else:
                    raise
            else:
                break

    def ready_checker(self):
        """Wait until the server is started.

        Annoyingly, there's no way to get a callback to be run when the Flask
        server starts.  Instead, we'll have to poll.
        """

        while True:
            if self.port:
                try:
                    response = requests.get("http://%s:%s/ping" % (self.host, self.port))
                    if response.status_code == 200:
                        break
                except socket.error as e:
                    if e.errno == errno.ECONNREFUSED:
                        pass
                    else:
                        raise

            time.sleep(0.1)

    def start_server(self):
        """Start the API server.

        returns: port (int) -- the port that the server is listening on
                   (on localhost)
        """

        checker = Thread(target=self.ready_checker)
        checker.start()
        self.start()
        checker.join()

        return self.port

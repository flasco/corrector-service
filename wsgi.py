# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

import os

from app import app

PORT = int(os.environ.get('FLASK_APP_PORT') or 3000)

# Uncomment the following line to redirect HTTP requests to HTTPS.
application = app

if __name__ == '__main__':
    from gevent.pywsgi import WSGIServer

    env = os.environ.get('FLASK_APP_ENV') or 'dev'
    if env == 'production':
        server = WSGIServer(('0.0.0.0', PORT), application)
        server.serve_forever()
    else:
        from werkzeug._reloader import run_with_reloader
        from werkzeug.debug import DebuggedApplication

        app.debug = True
        application = DebuggedApplication(application, evalex=True)
        address = 'localhost' if env == 'development' else '0.0.0.0'
        server = WSGIServer((address, PORT), application)
        run_with_reloader(server.start)

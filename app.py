# coding: utf-8
import sys
from datetime import datetime
import json
import leancloud
from flask import Flask, jsonify, request
from flask import render_template
from leancloud import LeanCloudError

from core.corrector import check_corrector

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/time')
def time():
    return str(datetime.now())


@app.route('/version')
def print_version():
    import sys
    return sys.version


# REST API example
class BadGateway(Exception):
    status_code = 502

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return jsonify(rv)


class BadRequest(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return jsonify(rv)


@app.errorhandler(BadGateway)
def handle_bad_gateway(error):
    response = error.to_json()
    response.status_code = error.status_code
    return response


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    response = error.to_json()
    response.status_code = error.status_code
    return response

@app.route('/api/python-version', methods=['GET'])
def python_version():
    return jsonify({"python-version": sys.version})

@app.route('/api/corrector', methods=['POST'])
def check_correct():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    content = data['content']
    if len(content) > 512:
        raise BadRequest('content length should less than 512')
    result = check_corrector(content)
    return jsonify({ "data": result })
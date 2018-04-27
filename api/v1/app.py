#!/usr/bin/python3
"""
Module for flask web framework
"""

from models import storage
from flask import Flask, jsonify, make_response
from api.v1.views import app_views
import os
app = Flask(__name__)
host = os.getnev('HBNB_API_HOST', default='0.0.0.0')
port = int(os.getnev('HBNB_API_PORT', default='5000'))
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_dat_sess(exception):
    '''
    Method to close a session
    '''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    '''
    Method for a 404 error
    '''
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    app.run(host=host, port=port)

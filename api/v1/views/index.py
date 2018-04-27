#!/usr/bin/python3
'''Module for main page'''
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    '''
    Method to find the status of the website
    '''

    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    '''
    Method for statistics of classes in database
    '''

    count_dict = {}
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    for key, value in classes.items():
        v = storage.count(value)
        count_dict[key] = v
    return jsonify(count_dict)

if __name__ == '__main__':
    pass

#!/usr/bin/python3
'''Module to render Place related information'''

from flask import request, jsonify, abort
from models import storage, classes
from api.v1.views import app_views


@app_views.route('/cities/<c_id>/places', strict_slashes=False,
                 methods=['GET'])
def all_objects_place(c_id):
    '''
    Method for a Get request for place objects
    Returns: json representation of dictionary of attributes for
    all instances in place
    '''
    ret_obj = storage.get("City", c_id)
    if ret_obj is None:
        abort(404)
    all_places = storage.all('Place')
    city_in_places = []
    for key, value in all_places.items():
        if value.city_id == c_id:
            city_in_places.append(value.to_dict())
    return (jsonify(city_in_places))


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def retrieve_by_id_place(place_id=None):
    '''
    Method for Get request for user objects according to user id (variable)
    Return: retrieved instance of User
    '''
    ret_obj = storage.get("Place", place_id)
    if ret_obj is None:
        abort(404)
    else:
        return jsonify(ret_obj.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_request_place(place_id=None):
    '''
    Method for Delete request for place objects according to
    place id (variable)
    Return: Empty dictionary
    '''
    ret_obj = storage.get("Place", place_id)
    if ret_obj is None:
        abort(404)
    else:
        storage.delete(ret_obj)
        return jsonify({}), 200


@app_views.route('/cities/<c_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_request_place(c_id):
    '''
    Method for Get request for place objects according to city id (variable)
    Return: retrieved instance of Place
    '''
    post_reqs = request.get_json()
    if post_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in post_reqs:
        return jsonify({"error": "Missing user_id"}), 400
    elif "name" not in post_reqs:
        return jsonify({"error": "Missing name"}), 400
    city = storage.get("City", c_id)
    user = storage.get("User", post_reqs["user_id"])
    if city is None or user is None:
        abort(404)
    else:
        post_reqs['city_id'] = c_id
        new_instance = classes["Place"](**post_reqs)
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def put_request_place(place_id):
    '''
    Method for update instance request for palce objects
    according to place id (variable)
    Return: retrieved instance of User
    '''
    put_reqs = request.get_json()
    if put_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    ret_place = storage.get("Place", place_id)
    if ret_place is None:
        abort(404)
    else:
        put_reqs.pop('updated_at', None)
        put_reqs.pop('created_at', None)
        put_reqs.pop('id', None)
        put_reqs.pop('user_id', None)
        put_reqs.pop('city_id', None)
        for key, value in put_reqs.items():
            setattr(ret_place, key, value)
        ret_place.save()
        return (jsonify(ret_place.to_dict()), 200)

if __name__ == '__main__':
    pass

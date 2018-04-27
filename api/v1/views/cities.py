#!/usr/bin/python3
'''Module to render State related information'''

from flask import request, jsonify, abort
from models import storage, classes, City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def retrieve_all_cities(state_id=None):
    '''
    Method for Get request for state objects according to state id (variable)
    Return: retrieved instance of State
    '''
    city_list = []
    ret_state = storage.get("State", state_id)
    if ret_state is None:
        abort(404)
    else:
        all_cities = ret_state.cities
        for obj in all_cities:
            city_list.append(obj.to_dict())
        return jsonify(city_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_with_id(city_id):
    '''
    Method for a Get request for state objects
    Returns: json representation of dictionary of attributes for
    all instances in state
    '''
    ret_city = storage.get("City", city_id)
    if ret_city is None:
        abort(404)
    else:
        return (jsonify(ret_city.to_dict()))


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    '''
    Method for Delete request for state objects according to
    state id (variable)
    Return: Empty dictionary
    '''
    ret_obj = storage.get("City", city_id)
    if ret_obj is None:
        abort(404)
    else:
        storage.delete(ret_obj)
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    '''
    Method for Get request for state objects according to state id (variable)
    Return: retrieved instance of State
    '''
    post_reqs = request.get_json()
    if post_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in post_reqs:
        return jsonify({"error": "Missing name"}), 400
    else:
        try:
            post_reqs["state_id"] = state_id
            new_instance = classes["City"](**post_reqs)
            new_instance.save()
            return jsonify(new_instance.to_dict()), 201
        except:
            abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    '''
    Method for update instance request for state objects
    according to state id (variable)
    Return: retrieved instance of State
    '''
    put_reqs = request.get_json()
    ret_city = storage.get("City", city_id)
    if put_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        try:
            put_reqs.pop('updated_at', None)
            put_reqs.pop('created_at', None)
            put_reqs.pop('id', None)
            for key, value in put_reqs.items():
                setattr(state, key, value)
            ret_city.save()
            return (jsonify(state.to_dict()), 200)
        except:
            abort(404)

if __name__ == '__main__':
    pass

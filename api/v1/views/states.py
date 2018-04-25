#!/usr/bin/python3
'''Module to render State related information'''

from flask import request, jsonify, abort
from models import storage, classes
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_objects():
    '''
    Method for a Get request for state objects
    Returns: json representation of dictionary of attributes for
    all instances in state
    '''
    states_dict = storage.all("State")
    states_list = []
    for key, value in states_dict.items():
        states_list.append(value.to_dict())
    return (jsonify(states_list))


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def retrieve_by_id(state_id=None):
    '''
    Method for Get request for state objects according to state id (variable)
    Return: retrieved instance of State
    '''

    ret_state = storage.get("State", state_id)
    if ret_state is None:
        abort(404)
    else:
        return jsonify(ret_state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_request(state_id=None):
    '''
    Method for Delete request for state objects according to
    state id (variable)
    Return: Empty dictionary
    '''
    ret_obj = storage.get("State", state_id)
    if ret_obj is None:
        abort(404)
    else:
        storage.delete(ret_obj)
        return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_request():
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
        new_instance = classes["State"](**post_reqs)
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def put_request(state_id):
    '''
    Method for update instance request for state objects
    according to state id (variable)
    Return: retrieved instance of State
    '''
    put_reqs = request.get_json()
    state = storage.get("State", state_id)
    if put_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        try:
            put_reqs.pop('updated_at', None)
            put_reqs.pop('created_at', None)
            put_reqs.pop('id', None)
            for key, value in put_reqs.items():
                setattr(state, key, value)
                state.save()
            return (jsonify(state.to_dict()), 200)
        except:
            abort(404)

if __name__ == '__main__':
    pass

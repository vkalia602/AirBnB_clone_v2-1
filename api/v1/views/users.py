#!/usr/bin/python3                                                                                                                                                                                        
'''Module to render User related information'''

from flask import request, jsonify, abort
from models import storage, classes
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_objects_user():
    '''
    Method for a Get request for user objects
    Returns: json representation of dictionary of attributes for
    all instances in user
    '''
    users_dict = storage.all("User")
    users_list = []
    for key, value in users_dict.items():
        users_list.append(value.to_dict())
    return (jsonify(users_list))


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def retrieve_by_id_user(user_id=None):
    '''
    Method for Get request for user objects according to user id (variable)
    Return: retrieved instance of User
    '''

    ret_user = storage.get("User", user_id)
    if ret_user is None:
        abort(404)
    else:
        return jsonify(ret_user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_request_user(user_id=None):
    '''
    Method for Delete request for user objects according to
    user id (variable)
    Return: Empty dictionary
    '''
    ret_obj = storage.get("User", user_id)
    if ret_obj is None:
        abort(404)
    else:
        storage.delete(ret_obj)
        return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_request_user():
    '''
    Method for Get request for user objects according to user id (variable)
    Return: retrieved instance of Amenity
    '''
    post_reqs = request.get_json()
    if post_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "email" not in post_reqs:
        return jsonify({"error": "Missing email"}), 400
    elif "password" not in post_reqs:
        return jsonify({"error": "Missing password"}), 400
    else:
        new_instance = classes["User"](**post_reqs)
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_request_user(user_id):
    '''
    Method for update instance request for user objects
    according to user id (variable)
    Return: retrieved instance of User
    '''
    put_reqs = request.get_json()
    user = storage.get("User", user_id)
    if put_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        try:
            put_reqs.pop('updated_at', None)
            put_reqs.pop('created_at', None)
            put_reqs.pop('id', None)
            put_reqs.pop('email', None)
            for key, value in put_reqs.items():
                setattr(user, key, value)
            user.save()
            return (jsonify(user.to_dict()), 200)
        except:
            abort(404)

if __name__ == '__main__':
    pass

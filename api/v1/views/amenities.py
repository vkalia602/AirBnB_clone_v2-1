#!/usr/bin/python3
'''Module to render Amenity related information'''

from flask import request, jsonify, abort
from models import storage, classes
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_objects_amen():
    '''
    Method for a Get request for amenity objects
    Returns: json representation of dictionary of attributes for
    all instances in amenity
    '''

    amenities_dict = storage.all("Amenity")
    amenities_list = []
    for key, value in amenities_dict.items():
        amenities_list.append(value.to_dict())
    return (jsonify(amenities_list))


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_by_id_amen(amenity_id=None):
    '''
    Method for Get request for amenity objects according to amenity
    id (variable)
    Return: retrieved instance of Amenity
    '''

    ret_amenity = storage.get("Amenity", amenity_id)
    if ret_amenity is None:
        abort(404)
    else:
        return jsonify(ret_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_request_amen(amenity_id=None):
    '''
    Method for Delete request for amenity objects according to
    state id (variable)
    Return: Empty dictionary
    '''
    ret_obj = storage.get("Amenity", amenity_id)
    if ret_obj is None:
        abort(404)
    else:
        storage.delete(ret_obj)
        return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_request_amen():
    '''
    Method for Get request for amenity objects according to amenity id
    (variable)
    Return: retrieved instance of Amenity
    '''
    post_reqs = request.get_json()
    if post_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in post_reqs:
        return jsonify({"error": "Missing name"}), 400
    else:
        new_instance = classes["Amenity"](**post_reqs)
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def put_request_amen(amenity_id):
    '''
    Method for update instance request for amenity objects
    according to amenity id (variable)
    Return: retrieved instance of Amenity
    '''
    put_reqs = request.get_json()
    amenity = storage.get("Amenity", amenity_id)
    if put_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        try:
            put_reqs.pop('updated_at', None)
            put_reqs.pop('created_at', None)
            put_reqs.pop('id', None)
            for key, value in put_reqs.items():
                setattr(amenity, key, value)
            amenity.save()
            return (jsonify(amenity.to_dict()), 200)
        except:
            abort(404)

if __name__ == '__main__':
    pass

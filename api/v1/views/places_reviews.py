#!/usr/bin/python3                                                                                                                                                                                        
'''Module to render Place Reviews related information'''

from flask import request, jsonify, abort
from models import storage, classes
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['GET'])
def all_objects():
    '''
    Method for a Get request for place objects
    Returns: json representation of dictionary of attributes for
    all instances in place
    '''
    ret_obj = storage.get("Place", place_id)
    if ret_obj is None:
        abort(404)
    all_places = storage.all('Reviews')
    review_list = []
    for key, value in all_places.items():
        if value.place.id == place_id:
            review_list.append(value.to_json())
    return (jsonify(review_list))


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def retrieve_by_id(review_id=None):
    '''
    Method for Get request for review objects according to user id (variable)
    Return: retrieved instance of review
    '''
    ret_obj = storage.get("Review", review_id)
    if ret_user is None:
        abort(404)
    else:
        return jsonify(ret_obj.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_request(place_id=None):
    '''
    Method for Delete request for review objects according to
    review id (variable)
    Return: Empty dictionary
    '''
    ret_obj = storage.get("Review", review_id)
    if ret_obj is None:
        abort(404)
    else:
        storage.delete(ret_obj)
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST'])
def create_request():
    '''
    Method for Get request for review objects according to place id (variable)
    Return: retrieved instance of Review
    '''
    post_reqs = request.get_json()
    if post_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in post_reqs:
        return jsonify({"error": "Missing user_id"}), 400
    elif "text" not in post_reqs:
        return jsonify({"error": "Missing text"}), 400
    place = storage.get("Place", place_id)
    user = storage.get("User", post_reqs["user_id"])
    if place is None or user is None:
        abort(404)
    else:
        new_instance = classes["Review"](**post_reqs)
        new_instance.save()
        return jsonify(new_instance.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def put_request(review_id):
    '''
    Method for update instance request for review objects
    according to review id (variable)
    Return: retrieved instance of Review
    '''
    put_reqs = request.get_json()
    review = storage.get("Review", review_id)
    if put_reqs is None:
        return jsonify({"error": "Not a JSON"}), 400
    else:
        try:
            put_reqs.pop('updated_at', None)
            put_reqs.pop('created_at', None)
            put_reqs.pop('id', None)
            put_reqs.pop('user_id', None)
            put_reqs.pop('place_id', None)
            for key, value in put_reqs.items():
                setattr(review, key, value)
                review.save()
            return (jsonify(review.to_dict()), 200)
        except:
            abort(404)

if __name__ == '__main__':
    pass

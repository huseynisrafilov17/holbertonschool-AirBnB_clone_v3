#!/usr/bin/python3
"""
Defines API endpoints for Place objects.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    cities = storage.all("City").values()
    city = list(filter(lambda x: x.id == city_id, cities))
    if len(city) == 0:
        abort(404)
    places = list(map(lambda x: x.to_dict(), city[0].places))
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                  strict_slashes=False))
def add_place(city_id):
    cities = storage.all("City").values()
    city = list(filter(lambda x: x.id == city_id, cities))
    if len(city) == 0:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    users = storage.all("User").values()
    user = list(filter(lambda x: x.id == user_id, users))
    if len(user) == 0:
        abort(404)
    new_place = Place()
    for key, value in data.items():
        setattr(place, key, value)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

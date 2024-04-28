#!/usr/bin/python3
"""
Defines API endpoints for Place objects.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects of a City"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    elif request.method == 'POST':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        if 'name' not in data:
            abort(400, 'Missing name')
        user = storage.get(User, data['user_id'])
        if not user:
            abort(404)
        data['city_id'] = city_id
        new_place = Place(**data)
        new_place.save()
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

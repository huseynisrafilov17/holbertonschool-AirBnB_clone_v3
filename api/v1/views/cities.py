#!/usr/bin/python3
"""State api methods"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
import json


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def cities(state_id):
    states = storage.all("State").values()
    state = list(filter(lambda x: x.id == state_id, states))
    if len(state) == 0:
        abort(404)
    else:
        cities = state[0].cities
        cities_json = list(map(lambda x: x.to_dict(), cities))
        return jsonify(cities_json)


@app_views.route("cities/<city_id>", methods=["GET"], strict_slashes=False)
def city(city_id):
    cities = storage.all("City").values()
    city = list(filter(lambda x: x.id == city_id, cities))
    if len(city) == 0:
        abort(404)
    else:
        return jsonify(city[0].to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def city_delete(city_id):
    cities = storage.all("City").values()
    city = list(filter(lambda x: x.id == city_id, cities))
    if len(city) == 0:
        abort(404)
    else:
        city[0].delete()
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_add(state_id):
    states = storage.all("State").values()
    state = list(filter(lambda x: x.id == state_id, states))
    if len(state) == 0:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "name" not in data.keys():
        abort(400, 'Missing name')
    new_city = City()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(new_city, key, value)
    new_city.state_id = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def city_update(city_id):
    cities = storage.all("City").values()
    city = list(filter(lambda x: x.id == city_id, cities))
    if len(city) == 0:
        abort(404)
    else:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(city[0], key, value)
        storage.save()
        return jsonify(city[0].to_dict()), 200

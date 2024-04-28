#!/usr/bin/python3
"""Amenity api methods"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
import json


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenities():
    amenities = storage.all("Amenity").values()
    amenities_list = list(map(lambda x: x.to_dict(), amenities))
    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def amenity(amenity_id):
    amenities = storage.all("Amenity").values()
    amenity = list(filter(lambda x: x.id == amenity_id, amenities))
    if len(amenity) == 0:
        abort(404)
    else:
        return jsonify(amenity[0].to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    amenities = storage.all("Amenity").values()
    amenity = list(filter(lambda x: x.id == amenity_id, amenities))
    if len(amenity) == 0:
        abort(404)
    else:
        amenity[0].delete()
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_add():
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "name" not in data.keys():
        abort(400, 'Missing name')
    new_amenity = Amenity()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(new_amenity, key, value)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def amenity_update(amenity_id):
    amenities = storage.all("Amenity").values()
    amenity = list(filter(lambda x: x.id == amenity_id, amenities))
    if len(amenity) == 0:
        abort(404)
    else:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity[0], key, value)
        storage.save()
        return jsonify(amenity[0].to_dict()), 200

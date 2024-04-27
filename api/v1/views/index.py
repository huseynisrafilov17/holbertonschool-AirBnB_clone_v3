#!/usr/bin/python3
"""Index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    counts = ["Amenity", "City", "Place", "Review", "State", "User"]
    keys = ["amenities", "cities", "places", "reviews", "states", "users"]
    dictionary = {}
    for i in range(0, len(counts)):
        dictionary[keys[i]] = storage.count(counts[i])

    return jsonify(dictionary)

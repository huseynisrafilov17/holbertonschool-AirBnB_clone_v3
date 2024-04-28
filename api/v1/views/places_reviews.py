#!/usr/bin/python3
"""Reviews api methods"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
import json


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def reviews(place_id):
    places = storage.all("Place").values()
    place = list(filter(lambda x: x.id == place_id, places))
    if len(place) == 0:
        abort(404)
    reviews = list(map(lambda x: x.to_dict(), place[0].reviews))
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def review(review_id):
    reviews = storage.all("Review").values()
    review = list(filter(lambda x: x.id == review_id, reviews))
    if len(review) == 0:
        abort(404)
    else:
        return jsonify(review[0].to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def review_delete(review_id):
    reviews = storage.all("Review").values()
    review = list(filter(lambda x: x.id == review_id, reviews))
    if len(review) == 0:
        abort(404)
    else:
        review[0].delete()
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_add(place_id):
    places = storage.all("Place").values()
    place = list(filter(lambda x: x.id == place_id, places))
    if len(place) == 0:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "user_id" not in data.keys():
        abort(400, 'Missing user_id')
    users = storage.all("User").values()
    user = list(filter(lambda x: x.id == data["user_id"], users))
    if len(user) == 0:
        abort(404)
    if "text" not in data.keys():
        abort(400, 'Missing text')
    new_review = Review()
    new_review.place_id = place_id
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(new_state, key, value)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def review_update(review_id):
    reviews = storage.all("Review").values()
    reviews = list(filter(lambda x: x.id == review_id, reviews))
    if len(review) == 0:
        abort(404)
    else:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in ignore:
                setattr(review[0], key, value)
        storage.save()
        return jsonify(review[0].to_dict()), 200

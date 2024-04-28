#!/usr/bin/python3
"""User api methods"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
import json


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    users = storage.all("User").values()
    users_list = list(map(lambda x: x.to_dict(), users))
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user(user_id):
    users = storage.all("User").values()
    user = list(filter(lambda x: x.id == user_id, users))
    if len(user) == 0:
        abort(404)
    else:
        return jsonify(user[0].to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def user_delete(user_id):
    users = storage.all("User").values()
    user = list(filter(lambda x: x.id == user_id, users))
    if len(user) == 0:
        abort(404)
    else:
        user[0].delete()
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_add():
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "email" not in data.keys():
        abort(400, 'Missing email')
    if "password" not in data.keys():
        abort(400, 'Missing password')
    new_user = User()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(new_user, key, value)
    storage.new(new_user)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_update(user_id):
    users = storage.all("User").values()
    user = list(filter(lambda x: x.id == user_id, users))
    if len(user) == 0:
        abort(404)
    else:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(user[0], key, value)
        storage.save()
        return jsonify(user[0].to_dict()), 200

#!/usr/bin/python3
"""State api methods"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    states = storage.all("State").values()
    states_list = list(map(lambda x: x.to_dict(), states))
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state(state_id):
    states = storage.all("State").values()
    state = list(filter(lambda x: x.id == state_id, states))
    if len(state) == 0:
        abort(404)
    else:
        return jsonify(state[0].to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete(state_id):
    states = storage.all("State").values()
    state = list(filter(lambda x: x.id == state_id, states))
    if len(state) == 0:
        abort(404)
    else:
        storage.delete(state[0])
        return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_add():
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if "name" not in data.keys():
        abort(400, 'Missing name')
    new_state = State(data)
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_update(state_id):
    states = storage.all("State").values()
    state = list(filter(lambda x: x.id == state_id, states))
    if len(state) == 0:
        abort(404)
    else:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                state[0].setattr(key, value)
        return jsonify(state[0].to_dict()), 200

#!/usr/bin/python3
"""An API"""
from flask import Flask, Blueprint, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_db(exc):
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", '0.0.0.0')
    port = getenv("HBNB_API_PORT", '5000')
    app.run(host, port, threaded=True)

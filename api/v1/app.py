#!/usr/bin/python3
"""
instantiate Flask app
register the blueprint
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found"}), 404)


@app.teardown_appcontext
def route_close(self):
    storage.close()

if __name__ == "__main__":
    app.run(host=os.environ.get('HBNB_API_HOST', '0.0.0.0'),
            port=os.environ.get('HBNB_API_PORT', '5000'))

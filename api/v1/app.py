#!/usr/bin/python3
"""
instantiate Flask app
register the blueprint
"""
from flask import Flask
from models import storage
from flask import jsonify
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return (jsonify({"error": "Not Found"}), 404)


@app.teardown_appcontext
def route_close(exception):
    storage.close()

if __name__ == "__main__":
    app.run(host=os.environ.get('HBNB_API_HOST'),
            port=os.environ.get('HBNB_API_PORT'))
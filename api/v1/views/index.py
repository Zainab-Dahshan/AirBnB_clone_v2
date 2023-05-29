#!/usr/bin/python3
"""index creating a route to status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """returns status"""
    return jsonify({'status': 'OK'})

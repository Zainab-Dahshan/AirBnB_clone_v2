#!/usr/bin/python3
"""The api module for city"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, State, City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """"Retrieves all cities and objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a specific city object id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a specific City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<city_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new City and its objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
        city = City(**data)
        city.state_id = state_id
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """updates the new city id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(404, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(City, key value)
    storage.save()
    return jsonify(city.to_dict()), 200

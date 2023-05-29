#!/usr/bin/python3
"""module for State restuful api"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, State


@app_views.route('/states',  methods=['GET'])
def get_states():
    """retreving all states"""
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    return jsdonify(state_list)


@app_viewa.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """retreving state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """creating a new state"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def upadate_state(state_id):
    """updating the state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

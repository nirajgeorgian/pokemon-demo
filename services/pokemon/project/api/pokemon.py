# services/pokemon/project/api/pokemon.py

from flask import Blueprint, jsonify

from project.api.models import Pokemon
from project import db

pokemon_blueprint = Blueprint('pokemon', __name__)

@pokemon_blueprint.route('/pokemon/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@pokemon_blueprint.route('/pokemon', methods=['GET'])
def pokemon():
    """Get all pokemon"""
    response_object = {
        'status': 'success',
        'data': {
            'pokemon': [pokemon.to_json() for pokemon in Pokemon.query.all()]
        }
    }
    return jsonify(response_object), 200

"""
Routes for /pet-types and /pet-types/{id}
"""
from flask import Blueprint, request, jsonify
from models import store
from utils import (
    get_animal_info_from_ninja,
    create_pet_type_from_ninja,
    filter_pet_types
)

pet_types_bp = Blueprint('pet_types', __name__)


@pet_types_bp.route('/pet-types', methods=['POST'])
def create_pet_type():
    """Create a new pet type"""
    # Check Content-Type
    if request.content_type != 'application/json':
        return jsonify({"error": "Expected application/json media type"}), 415
    
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Malformed data"}), 400
    
    if not data or 'type' not in data:
        return jsonify({"error": "Malformed data"}), 400
    
    pet_type_name = data['type']
    
    # Check if pet type already exists
    if store.pet_type_exists(pet_type_name):
        return jsonify({"error": "Malformed data"}), 400
    
    # Get info from Ninja API
    success, result = get_animal_info_from_ninja(pet_type_name)
    
    if not success:
        if result == 400:
            return jsonify({"error": "Malformed data"}), 400
        else:
            return jsonify({"server error": f"API response code {result}"}), 500
    
    # Create pet type object
    pet_type_id = store.get_next_id()
    pet_type = create_pet_type_from_ninja(pet_type_name, pet_type_id, result)
    
    # Store it
    store.add_pet_type(pet_type)
    
    # Return without internal fields
    response = {k: v for k, v in pet_type.items() if k != 'pet_details'}
    return jsonify(response), 201


@pet_types_bp.route('/pet-types', methods=['GET'])
def get_pet_types():
    """Get all pet types, with optional filtering"""
    pet_types = store.get_all_pet_types()
    
    # Filter based on query parameters
    query_params = request.args.to_dict()
    if query_params:
        pet_types = filter_pet_types(pet_types, query_params)
    
    # Remove internal fields
    response = [{k: v for k, v in pt.items() if k != 'pet_details'} for pt in pet_types]
    return jsonify(response), 200


@pet_types_bp.route('/pet-types/<id>', methods=['GET'])
def get_pet_type(id):
    """Get a specific pet type by ID"""
    pet_type = store.get_pet_type(id)
    
    if not pet_type:
        return jsonify({"error": "Not found"}), 404
    
    # Remove internal fields
    response = {k: v for k, v in pet_type.items() if k != 'pet_details'}
    return jsonify(response), 200


@pet_types_bp.route('/pet-types/<id>', methods=['DELETE'])
def delete_pet_type(id):
    """Delete a pet type by ID"""
    pet_type = store.get_pet_type(id)
    
    if not pet_type:
        return jsonify({"error": "Not found"}), 404
    
    # Check if pets array is not empty
    if pet_type['pets']:
        return jsonify({"error": "Malformed data"}), 400
    
    store.delete_pet_type(id)
    return '', 204


@pet_types_bp.route('/pet-types/<id>', methods=['PUT'])
def update_pet_type(id):
    """PUT is not allowed on /pet-types/{id}"""
    return jsonify({"error": "Method not allowed"}), 405

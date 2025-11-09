"""
Routes for /pet-types/{id}/pets and /pet-types/{id}/pets/{name}
"""
from flask import Blueprint, request, jsonify
from models import store
from utils import download_image, filter_pets
import os
import uuid

pets_bp = Blueprint('pets', __name__)


def generate_filename(pet_name, url):
    """Generate a unique filename for a pet picture"""
    # Get extension from URL
    ext = url.split('.')[-1].split('?')[0]  # Handle query params in URL
    if ext.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
        ext = 'jpg'  # Default to jpg
    
    # Create filename: petname-uuid.ext
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{pet_name}-{unique_id}.{ext}"
    return filename


@pets_bp.route('/pet-types/<id>/pets', methods=['POST'])
def create_pet(id):
    """Create a new pet for a pet type"""
    # Check if pet type exists
    pet_type = store.get_pet_type(id)
    if not pet_type:
        return jsonify({"error": "Not found"}), 404
    
    # Check Content-Type
    if request.content_type != 'application/json':
        return jsonify({"error": "Expected application/json media type"}), 415
    
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Malformed data"}), 400
    
    if not data or 'name' not in data:
        return jsonify({"error": "Malformed data"}), 400
    
    pet_name = data['name']
    
    # Check if pet name already exists for this type
    if store.pet_name_exists(id, pet_name):
        return jsonify({"error": "Malformed data"}), 400
    
    # Create pet object
    pet = {
        "name": pet_name,
        "birthdate": data.get('birthdate', 'NA'),
        "picture": "NA"
    }
    
    # Handle picture URL if provided
    if 'picture-url' in data:
        picture_url = data['picture-url']
        filename = generate_filename(pet_name, picture_url)
        success, result = download_image(picture_url, filename)
        
        if success:
            pet['picture'] = filename
        # If download fails, picture remains "NA"
    
    # Store pet
    store.add_pet_to_type(id, pet)
    store.update_pet(id, pet_name, pet)
    
    return jsonify(pet), 201


@pets_bp.route('/pet-types/<id>/pets', methods=['GET'])
def get_pets(id):
    """Get all pets for a pet type"""
    # Check if pet type exists
    pets = store.get_all_pets(id)
    if pets is None:
        return jsonify({"error": "Not found"}), 404
    
    # Filter based on query parameters
    query_params = request.args.to_dict()
    if query_params:
        pets = filter_pets(pets, query_params)
    
    return jsonify(pets), 200


@pets_bp.route('/pet-types/<id>/pets/<name>', methods=['GET'])
def get_pet(id, name):
    """Get a specific pet by name"""
    # Check if pet type exists
    if not store.get_pet_type(id):
        return jsonify({"error": "Not found"}), 404
    
    pet = store.get_pet(id, name)
    if not pet:
        return jsonify({"error": "Not found"}), 404
    
    return jsonify(pet), 200


@pets_bp.route('/pet-types/<id>/pets/<name>', methods=['DELETE'])
def delete_pet(id, name):
    """Delete a specific pet"""
    # Check if pet type exists
    if not store.get_pet_type(id):
        return jsonify({"error": "Not found"}), 404
    
    pet = store.delete_pet(id, name)
    if not pet:
        return jsonify({"error": "Not found"}), 404
    
    # Delete picture file if it exists
    if pet['picture'] != 'NA':
        picture_path = f"pictures/{pet['picture']}"
        if os.path.exists(picture_path):
            os.remove(picture_path)
    
    return '', 204


@pets_bp.route('/pet-types/<id>/pets/<name>', methods=['PUT'])
def update_pet(id, name):
    """Update a pet's information"""
    # Check if pet type exists
    pet_type = store.get_pet_type(id)
    if not pet_type:
        return jsonify({"error": "Not found"}), 404
    
    # Check if pet exists
    existing_pet = store.get_pet(id, name)
    if not existing_pet:
        return jsonify({"error": "Not found"}), 404
    
    # Check Content-Type
    if request.content_type != 'application/json':
        return jsonify({"error": "Expected application/json media type"}), 415
    
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Malformed data"}), 400
    
    if not data or 'name' not in data:
        return jsonify({"error": "Malformed data"}), 400
    
    # Name in payload must match URL name
    if data['name'].lower() != name.lower():
        return jsonify({"error": "Malformed data"}), 400
    
    # Update pet object
    updated_pet = {
        "name": name,
        "birthdate": data.get('birthdate', existing_pet['birthdate']),
        "picture": existing_pet['picture']
    }
    
    # Handle picture URL if provided
    if 'picture-url' in data:
        picture_url = data['picture-url']
        
        # Only download if URL is different or no picture exists
        need_download = True
        if existing_pet['picture'] != 'NA':
            # Check if it's the same URL (stored in pet data if needed)
            # For simplicity, we'll re-download unless URL hasn't changed
            # In production, you'd store the original URL to compare
            pass
        
        if need_download:
            filename = generate_filename(name, picture_url)
            success, result = download_image(picture_url, filename)
            
            if success:
                # Delete old picture if it exists
                if existing_pet['picture'] != 'NA':
                    old_path = f"pictures/{existing_pet['picture']}"
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                updated_pet['picture'] = filename
    
    # Store updated pet
    store.update_pet(id, name, updated_pet)
    
    return jsonify(updated_pet), 200

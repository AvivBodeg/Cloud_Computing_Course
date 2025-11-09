"""
Utility functions for Pet Store API
"""
import re
import requests
from datetime import datetime

# Your API Ninjas key - REPLACE THIS WITH YOUR ACTUAL KEY
NINJA_API_KEY = "pSgkQKYWrLDlQI0Sg3zmLQ==RrHpVdqh8aCzByaQ"

def get_animal_info_from_ninja(animal_type):
    """
    Fetch animal information from Ninja Animals API
    Returns (success, data_or_error_code)
    """
    url = "https://api.api-ninjas.com/v1/animals"
    headers = {'X-Api-Key': NINJA_API_KEY}
    params = {'name': animal_type}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            return False, response.status_code
        
        data = response.json()
        
        if not data:
            return False, 400  # Animal not found
        
        # Find exact match (case insensitive)
        animal_type_lower = animal_type.lower()
        exact_match = None
        
        for entry in data:
            if entry.get('name', '').lower() == animal_type_lower:
                exact_match = entry
                break
        
        if not exact_match:
            return False, 400  # No exact match found
        
        return True, exact_match
        
    except Exception as e:
        return False, 500


def parse_attributes(ninja_data):
    """
    Extract attributes from temperament or group_behavior field
    Returns list of strings
    """
    # Try temperament first, then group_behavior
    attr_text = ninja_data.get('temperament') or ninja_data.get('group_behavior')
    
    if not attr_text:
        return []
    
    # Remove punctuation and split into words
    words = re.sub(r'[^\w\s]', ' ', attr_text).split()
    return words


def parse_lifespan(ninja_data):
    """
    Extract lifespan as integer from Ninja API data
    Returns integer or None
    """
    lifespan_text = ninja_data.get('lifespan')
    
    if not lifespan_text:
        return None
    
    # Extract all numbers from the text
    numbers = re.findall(r'\d+', lifespan_text)
    
    if not numbers:
        return None
    
    # Return the lowest number
    return int(min(numbers, key=int))


def create_pet_type_from_ninja(pet_type_name, pet_type_id, ninja_data):
    """
    Create a pet-type JSON object from Ninja API data
    """
    return {
        "id": pet_type_id,
        "type": pet_type_name,
        "family": ninja_data.get('taxonomy', {}).get('family', ''),
        "genus": ninja_data.get('taxonomy', {}).get('genus', ''),
        "attributes": parse_attributes(ninja_data),
        "lifespan": parse_lifespan(ninja_data),
        "pets": [],
        "pet_details": {}  # Internal storage for pet objects
    }


def download_image(url, filename):
    """
    Download image from URL and save to file
    Returns (success, filename_or_error)
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False, "Failed to download image"
        
        # Save the image
        filepath = f"pictures/{filename}"
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        return True, filename
        
    except Exception as e:
        return False, str(e)


def parse_date(date_str):
    """
    Parse date in DD-MM-YYYY format
    Returns datetime object or None
    """
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except:
        return None


def filter_pet_types(pet_types, query_params):
    """
    Filter pet types based on query parameters
    """
    filtered = pet_types
    
    for key, value in query_params.items():
        if key == 'hasAttribute':
            # Case insensitive attribute matching
            value_lower = value.lower()
            filtered = [
                pt for pt in filtered
                if any(attr.lower() == value_lower for attr in pt['attributes'])
            ]
        elif key in ['id', 'type', 'family', 'genus']:
            # Case insensitive string matching
            value_lower = value.lower()
            filtered = [
                pt for pt in filtered
                if pt[key].lower() == value_lower
            ]
        elif key == 'lifespan':
            # Numeric matching
            try:
                lifespan_val = int(value)
                filtered = [
                    pt for pt in filtered
                    if pt['lifespan'] == lifespan_val
                ]
            except ValueError:
                pass
    
    return filtered


def filter_pets(pets, query_params):
    """
    Filter pets based on query parameters (birthdateGT, birthdateLT)
    """
    filtered = pets
    
    if 'birthdateGT' in query_params:
        date_gt = parse_date(query_params['birthdateGT'])
        if date_gt:
            filtered = [
                pet for pet in filtered
                if pet['birthdate'] != 'NA' and parse_date(pet['birthdate']) and parse_date(pet['birthdate']) > date_gt
            ]
    
    if 'birthdateLT' in query_params:
        date_lt = parse_date(query_params['birthdateLT'])
        if date_lt:
            filtered = [
                pet for pet in filtered
                if pet['birthdate'] != 'NA' and parse_date(pet['birthdate']) and parse_date(pet['birthdate']) < date_lt
            ]
    
    return filtered

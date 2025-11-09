"""
Pet Store Models and In-Memory Data Storage
"""

class PetStoreData:
    """In-memory storage for pet store data"""
    def __init__(self):
        self.pet_types = {}  # {id: pet_type_dict}
        self.next_id = 1
        self.used_ids = set()  # Track used IDs to never reuse them
        
    def get_next_id(self):
        """Generate next unique ID"""
        id_str = str(self.next_id)
        self.next_id += 1
        self.used_ids.add(id_str)
        return id_str
    
    def add_pet_type(self, pet_type):
        """Add a pet type to storage"""
        self.pet_types[pet_type['id']] = pet_type
        
    def get_pet_type(self, id):
        """Get pet type by ID"""
        return self.pet_types.get(id)
    
    def get_all_pet_types(self):
        """Get all pet types"""
        return list(self.pet_types.values())
    
    def delete_pet_type(self, id):
        """Delete pet type by ID"""
        if id in self.pet_types:
            del self.pet_types[id]
            return True
        return False
    
    def pet_type_exists(self, type_name):
        """Check if pet type already exists (case insensitive)"""
        type_name_lower = type_name.lower()
        for pet_type in self.pet_types.values():
            if pet_type['type'].lower() == type_name_lower:
                return True
        return False
    
    def add_pet_to_type(self, pet_type_id, pet):
        """Add a pet to a pet type"""
        if pet_type_id in self.pet_types:
            self.pet_types[pet_type_id]['pets'].append(pet['name'])
            return True
        return False
    
    def get_pet(self, pet_type_id, pet_name):
        """Get a specific pet by name from a pet type"""
        pet_type = self.get_pet_type(pet_type_id)
        if not pet_type:
            return None
        
        # Pet names are stored in pets array
        if pet_name not in pet_type['pets']:
            return None
            
        # Pet details are stored separately
        return pet_type.get('pet_details', {}).get(pet_name)
    
    def get_all_pets(self, pet_type_id):
        """Get all pets of a specific type"""
        pet_type = self.get_pet_type(pet_type_id)
        if not pet_type:
            return None
        
        pet_details = pet_type.get('pet_details', {})
        return [pet_details[name] for name in pet_type['pets'] if name in pet_details]
    
    def delete_pet(self, pet_type_id, pet_name):
        """Delete a pet from a pet type"""
        pet_type = self.get_pet_type(pet_type_id)
        if not pet_type:
            return False
        
        if pet_name in pet_type['pets']:
            pet_type['pets'].remove(pet_name)
            if 'pet_details' in pet_type and pet_name in pet_type['pet_details']:
                pet_obj = pet_type['pet_details'][pet_name]
                del pet_type['pet_details'][pet_name]
                return pet_obj
        return None
    
    def update_pet(self, pet_type_id, pet_name, pet_data):
        """Update a pet's information"""
        pet_type = self.get_pet_type(pet_type_id)
        if not pet_type or pet_name not in pet_type['pets']:
            return False
        
        if 'pet_details' not in pet_type:
            pet_type['pet_details'] = {}
        
        pet_type['pet_details'][pet_name] = pet_data
        return True
    
    def pet_name_exists(self, pet_type_id, pet_name):
        """Check if pet name exists for a given type (case insensitive)"""
        pet_type = self.get_pet_type(pet_type_id)
        if not pet_type:
            return False
        
        pet_name_lower = pet_name.lower()
        return any(name.lower() == pet_name_lower for name in pet_type['pets'])


# Global data store instance
store = PetStoreData()

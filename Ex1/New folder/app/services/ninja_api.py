import os
from dotenv import load_dotenv
import requests
from typing import Optional, Dict, Any

load_dotenv()

class NinjaAPIService:
    def __init__(self):
        self.api_key = os.getenv("NINJA_API_KEY")
        self.base_url = "https://api.api-ninjas.com/v1/animals"
        
    def get_animal_info(self, animal_type: str) -> Optional[Dict[str, Any]]:
        headers = {
            'X-Api-Key': self.api_key
        }
        
        response = requests.get(
            self.base_url, 
            headers=headers, 
            params={'name': animal_type}
        )
        
        if response.status_code != 200:
            if response.status_code == 404:
                return None
            raise Exception(f"API response code {response.status_code}")
            
        animals = response.json()
        
        # Find exact match (case insensitive)
        for animal in animals:
            if animal.get('name', '').lower() == animal_type.lower():
                return animal
                
        return None

    def process_attributes(self, animal_data: Dict[str, Any]) -> list[str]:
        """Extract and process attributes from animal data"""
        if 'temperament' in animal_data:
            return [word.strip() for word in animal_data['temperament'].replace(',', ' ').split()]
        elif 'group_behavior' in animal_data:
            return [word.strip() for word in animal_data['group_behavior'].replace(',', ' ').split()]
        return []

    def process_lifespan(self, lifespan_str: str) -> Optional[int]:
        """Process lifespan string to extract the lowest number"""
        if not lifespan_str:
            return None
            
        # Remove "up to" and "years" text
        cleaned = lifespan_str.lower().replace('up to', '').replace('years', '').strip()
        
        # Handle ranges like "2 to 5" or "from 2 to 5"
        if 'to' in cleaned:
            numbers = [int(n) for n in cleaned.replace('from', '').split('to') if n.strip().isdigit()]
            return min(numbers) if numbers else None
            
        # Handle single numbers
        try:
            return int(''.join(filter(str.isdigit, cleaned)))
        except ValueError:
            return None
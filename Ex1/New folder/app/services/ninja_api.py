from dotenv import load_dotenv
from typing import Optional
import os
import requests
import re

"""
Service for interacting with the API Ninjas Animals API.
Handles API key loading, request logic, and response parsing.
"""

load_dotenv()

NINJA_API_KEY = os.getenv("NINJA_API_KEY")
API_URL = "https://api-ninjas.com/api/animals"

class NinjaAPIError(Exception):
    """Custom exception for Ninja API errors."""
    pass

class NinjaAPI:
    def __init__(self, api_key: Optional[str] = None):
        if api_key is None:
            api_key = NINJA_API_KEY
        if not api_key:
            raise ValueError("Ninja API key not found. Please set NINJA_API_KEY in your .env file.")
        self.api_key = api_key

    def fetch_animal(self, animal_type: str):
        """
        Fetch animal data from Ninja API by type.
        Returns the API response JSON or raises NinjaAPIError.
        """
        headers = {"X-Api-Key": self.api_key}
        params = {"name": animal_type}
        try:
            response = requests.get(API_URL, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise NinjaAPIError("Animal type not found in Ninja API.") #400
            else:
                raise NinjaAPIError(f"API error: {response.status_code}") #500
        except requests.RequestException as e:
            raise NinjaAPIError(f"Request failed: {str(e)}") #???

    def _parse_attributes(self, entry: dict) -> list:
        """Extract attributes array from 'temperament' or 'group_behavior'.
        Rules:
        - Prefer 'temperament' over 'group_behavior' when both exist.
        - Split the selected string into words.
        - Return empty list when neither field exists or value is empty.
        """
        text = None
        if 'temperament' in entry and entry.get('temperament'):
            text = entry.get('temperament')
        elif 'group_behavior' in entry and entry.get('group_behavior'):
            text = entry.get('group_behavior')

        if not text:
            return []

        cleaned = re.sub(r"[\.,;:!()\[\]{}\"]", ' ', text) # Remove punctuation
        cleaned = " ".join(cleaned.split()) # Normalize spaces
        parts = [p for p in cleaned.split() if p]
        return parts
    
    def _parse_lifespan(self, entry: dict) -> 'Optional[int]':
        """Parse lifespan string into an integer as per spec.
        Examples:
        - "up to 41 years" -> 41
        - "from 2 to 5 years" -> 2 (lowest number)
        - "12" -> 12
        - missing/empty -> None
        """
        text = entry.get('lifespan')
        if not text:
            return None
        
        # Find all integers in the string
        nums = [int(n) for n in re.findall(r"(\d+)", str(text))]
        return min(nums) if nums else None

    # TODO: review the code below
    def get_pet_type_info(self, animal_type: str) -> dict:
        """High-level method to fetch and normalize a pet-type from the Ninja API.

        Returns a dict with keys: type, family, genus, attributes (list), lifespan (int|null)
        Raises NinjaAPIError if not found or on API errors.
        """
        raw = self.fetch_animal(animal_type)

        if not isinstance(raw, list):
            raise NinjaAPIError("Unexpected API response format")

        # Find exact name match (case-insensitive)
        target = None
        for entry in raw:
            name = entry.get('name')
            if name and name.strip().lower() == animal_type.strip().lower():
                target = entry
                break

        if target is None:
            # If no exact match, consider API didn't find the specific animal
            raise NinjaAPIError("Animal type not found in Ninja API.")

        # Extract fields
        pet_type = target.get('name')
        # Permissive handling: if the Ninja API doesn't provide family/genus
        # we'll keep them as empty strings so the application can still
        # create a PetType. This is intentionally permissive; consider
        # switching to a strict behavior (raising an error) if you want
        # to enforce taxonomy completeness later.
        # TODO: revisit this decision before submission/grading.
        family = target.get('family') or ''
        genus = target.get('genus') or ''
        attributes = self._parse_attributes(target)
        lifespan = self._parse_lifespan(target)

        return {
            'type': pet_type,
            'family': family,
            'genus': genus,
            'attributes': attributes,
            'lifespan': lifespan,
        }

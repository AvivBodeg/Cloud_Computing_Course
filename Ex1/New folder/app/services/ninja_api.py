from dotenv import load_dotenv
from typing import Optional
import os
import requests
from app.schemas.pet_type_schema import PetTypeInfo
import re

"""
Service for interacting with the API Ninjas Animals API.
Handles API key loading, request logic, and response parsing.
"""

load_dotenv()

NINJA_API_KEY = os.getenv("NINJA_API_KEY")
API_URL = "https://api.api-ninjas.com/v1/animals"

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
        text = entry.get('temperament') or entry.get('group_behavior')
        if not text:
            return []

        text = re.sub(r"[^\w\s]", " ", text)
        return text.split()

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
    def get_pet_type_info(self, animal_type: str) -> PetTypeInfo:
        """Fetch and normalize a pet-type from the Ninja API.
        Returns a dict with the following keys: type, family, genus, attributes (list), lifespan (int|null)
        Raises NinjaAPIError if not found or on API errors.
        """
        raw = self.fetch_animal(animal_type)

        if not isinstance(raw, list):
            raise NinjaAPIError("Unexpected API response format")

        # Find exact name match (case-insensitive)
        target = None
        target = next(
            (entry for entry in raw if entry.get('name','').strip().lower() == animal_type.strip().lower()), None
            )
        
        if target is None:
            raise NinjaAPIError("Animal type not found in Ninja API.") #400

        # Extract fields
        pet_type = target.get('name')
        family = target.get('family') or ''
        genus = target.get('genus') or ''
        attributes = self._parse_attributes(target)
        lifespan = self._parse_lifespan(target)

        return PetTypeInfo(
            type=pet_type,
            family=family,
            genus=genus,
            attributes=attributes,
            lifespan=lifespan,
        )

from pydantic import Field, field_validator
from typing import List, Optional
from .base import ModelBase

"""
PetType Model

A classification model for different types of pets available in the store.
Contains information about different types of pets currently in inventory.

Example:
    {
        "id": "2",
        "type": "Poodle",
        "family": "Canidae",
        "genus": "Canis",
        "attributes": ["Intelligent", "alert", "active"],
        "lifespan": 16,
        "pets": ["Tony", "Lian", "Jamie"]
    }
"""

class PetType(ModelBase):
    id: str = Field(
        ...,
        description="Unique identifier for the pet type"
        )
    type: str = Field(
        ...,
        description="The type or breed of the pet",
        examples=["Poodle", "Golden Retriever", "Siamese Cat"]
        )
    family: str = Field(
        ...,
        description="The taxonomic family of the pet type",
        examples=["Canidae", "Felidae"]
        )
    genus: str = Field(
        ...,
        description="The taxonomic genus of the pet type",
        examples=["Canis", "Felis"]
        )
    attributes: List[str] = Field(
        ...,
        description="List of characteristics of the pet type (from temperament or group_behavior)",
        examples=[["Intelligent", "alert", "active"], ["Social", "playful"]]
        )
    lifespan: Optional[int] = Field(
        None,
        description="Average lifespan of the pet type in years (null if unknown)",
        examples=[16, 12, None]
        )
    pets: List[str] = Field(
        default_factory=list,
        description="List of names of pets belonging to this type currently in store",
        examples=[["Tony", "Lian", "Jamie"], []]  # Can be populated or empty
        )
        
    @field_validator('id')
    def validate_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Malformed data")
        return value
    
    @field_validator('type')
    def validate_type(cls, value: str) -> str:
        if not value:
            raise ValueError("Malformed data")
        return value
    
    @field_validator('family')
    def validate_family(cls, value: str) -> str:
        if not value:
            raise ValueError("Malformed data")
        return value

    @field_validator('genus')
    def validate_genus(cls, value: str) -> str:
        if not value:
            raise ValueError("Malformed data")
        return value
    
    @field_validator('lifespan')
    def validate_lifespan(cls, value: Optional[int]) -> Optional[int]:
        if value is None:
            return None
        if value <= 0:
            raise ValueError("Malformed data")
        return value
    
    @field_validator('pets')
    def validate_unique_pet_names(cls, value: List[str]) -> List[str]:
        # Check for duplicate names
        if len(value) != len(set(value)):
            raise ValueError("Malformed data")
        return value
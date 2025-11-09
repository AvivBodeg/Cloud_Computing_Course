from pydantic import Field, field_validator
from typing import Union, Literal
from datetime import datetime
import re
from .base import ModelBase

"""
Pet Model

A representation of a single pet in the store inventory.
Contains the pet's basic information such as name, birth date, and reference to its picture.

Example:
    {
        "name": "Jamie",
        "birthdate": "24-10-2023",
        "picture": "Jamie-poodle.jpg"
    }
"""

class Pet(ModelBase):
    name: str = Field(
        ...,
        description="The name of the pet"
        )
    birthdate: Union[str, Literal["NA"]] = Field(
        ...,
        description='Birthdate in "DD-MM-YYYY" format or "NA"',
        examples=["15-08-2020", "NA"]
        )
    picture: Union[str, Literal["NA"]] = Field(
        ...,
        description='Name of the file storing the image or "NA"',
        examples=["dog.png", "NA"]
        )
    
    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Malformed data")
        return value

    @field_validator('birthdate')
    def validate_birthdate(cls, value: str) -> str:
        if value == "NA":
            return "NA"
        try:
            pattern = r"^\d{2}-\d{2}-\d{4}$" # DD-MM-YYYY
            if not re.match(pattern, value):
                raise ValueError("Malformed data")
            datetime.strptime(value, "%d-%m-%Y") # Validate date
            return value
        except ValueError:
            raise ValueError("Malformed data")

    @field_validator('picture')
    def validate_picture(cls, value: str) -> str:
        if value == "NA":
            return "NA"
        if not value:
            raise ValueError("Malformed data")
        return value

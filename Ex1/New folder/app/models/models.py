from pydantic import BaseModel
from typing import List, Optional

class Pet(BaseModel):
    name: str
    birthdate: str = "NA"
    picture: str = "NA"

class PetType(BaseModel):
    id: str
    type: str
    family: str
    genus: str
    attributes: List[str]
    lifespan: Optional[int] = None
    pets: List[str] = []

class PetTypeCreate(BaseModel):
    type: str

class PetCreate(BaseModel):
    name: str
    birthdate: Optional[str] = "NA"
    picture_url: Optional[str] = None

class ErrorResponse(BaseModel):
    error: str
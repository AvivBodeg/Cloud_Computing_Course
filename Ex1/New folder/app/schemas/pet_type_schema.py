from typing import List, Optional
from pydantic import Field
from app.models.base import ModelBase

"""
DTOs for external / API models related to pet-types.

PetTypeInfo is a lightweight DTO representing the data we obtain
from the external Ninja API. It is intentionally permissive compared
to the domain `PetType` model.
"""


class PetTypeInfo(ModelBase):
    """Lightweight model returned by the Ninja API service.

    This model contains the fields obtained from the external API and is
    suitable for mapping into a full `PetType` (server-assigned `id` and
    `pets` list are not included here).
    """
    type: str = Field(
        ...,
        description="The type or breed of the pet",
        examples=["Poodle", "Golden Retriever", "Siamese Cat"]
        )
    family: str = Field(
        default="",
        description="The taxonomic family of the pet type (may be empty if missing from API)",
        examples=["Canidae", "Felidae", ""]
        )
    genus: str = Field(
        default="",
        description="The taxonomic genus of the pet type (may be empty if missing from API)",
        examples=["Canis", "Felis", ""]
        )
    attributes: List[str] = Field(
        default_factory=list,
        description="List of characteristics of the pet type (from temperament or group_behavior)",
        examples=[["Intelligent", "alert", "active"], ["Social", "playful"], []]
        )
    lifespan: Optional[int] = Field(
        None,
        description="Average lifespan of the pet type in years (null if unknown)",
        examples=[16, 12, None]
        )

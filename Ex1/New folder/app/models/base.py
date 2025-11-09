from pydantic import BaseModel, ConfigDict

"""
Module for shared model utilities and base classes.
"""

class ModelBase(BaseModel):
    """Base model with common configurations."""
    
    # Configure model behavior
    model_config = ConfigDict(
        str_strip_whitespace=False,
        str_to_lower=False,
        validate_assignment=True,
    )
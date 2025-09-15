#!/usr/bin/python3
"""
City module
Defines City class that inherits from BaseModel
"""

from models.base_model import BaseModel


class City(BaseModel):
    """City class that inherits from BaseModel"""

    state_id = ""
    name = ""

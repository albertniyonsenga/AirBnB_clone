#!/usr/bin/python3
"""
BaseModel module
Defines all common attributes/methods for other classes
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """Base class for all models in the AirBnB clone"""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel"""

        if kwargs:
            # Check if this is a reload from storage (has __class__ key)
            is_reload = "__class__" in kwargs

            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)

            # If it's not a reload, we still need to create id and timestamps
            if not is_reload:
                if not hasattr(self, 'id'):
                    self.id = str(uuid.uuid4())
                if not hasattr(self, 'created_at'):
                    self.created_at = datetime.now()
                if not hasattr(self, 'updated_at'):
                    self.updated_at = self.created_at
                models.storage.new(self)
        else:
            # Creating new instance
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Return string representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update updated_at and save the object"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return dictionary representation of the instance"""
        d = self.__dict__.copy()
        d["__class__"] = self.__class__.__name__
        d["created_at"] = self.created_at.isoformat()
        d["updated_at"] = self.updated_at.isoformat()
        return d

#!/usr/bin/python3
"""
FileStorage module
Serializes instances to a JSON file & deserializes back
"""

import json
from models.base_model import BaseModel


class FileStorage:
    """File storage engine"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all stored objects"""
        return self.__objects

    def new(self, obj):
        """Add new object to storage dictionary"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serialize objects to JSON file"""
        with open(self.__file_path, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, f)

    def reload(self):
        """Deserialize JSON file back to objects"""
        try:
            with open(self.__file_path, "r") as f:
                data = json.load(f)
                for obj in data.values():
                    cls_name = obj["__class__"]
                    if cls_name == "BaseModel":
                        self.new(BaseModel(**obj))
        except FileNotFoundError:
            pass

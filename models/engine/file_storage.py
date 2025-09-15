#!/usr/bin/python3
"""
FileStorage module
Serializes instances to a JSON file & deserializes back
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


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
                for obj_data in data.values():
                    cls_name = obj_data["__class__"]
                    if cls_name == "BaseModel":
                        self.new(BaseModel(**obj_data))
                    elif cls_name == "User":
                        self.new(User(**obj_data))
                    elif cls_name == "State":
                        self.new(State(**obj_data))
                    elif cls_name == "City":
                        self.new(City(**obj_data))
                    elif cls_name == "Amenity":
                        self.new(Amenity(**obj_data))
                    elif cls_name == "Place":
                        self.new(Place(**obj_data))
                    elif cls_name == "Review":
                        self.new(Review(**obj_data))
        except FileNotFoundError:
            pass

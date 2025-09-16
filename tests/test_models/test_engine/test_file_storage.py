#!/usr/bin/python3


import json
import os
import unittest
from unittest.mock import patch, mock_open

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine.file_storage import FileStorage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FileStorage()
        self.test_file = "test_file.json"

        # Reset the objects dictionary for each test
        self.storage._FileStorage__objects = {}
        self.storage._FileStorage__file_path = self.test_file

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_file_storage_instantiation(self):
        self.assertIsInstance(self.storage, FileStorage)
        self.assertEqual(self.storage._FileStorage__file_path, self.test_file)
        self.assertIsInstance(self.storage._FileStorage__objects, dict)

    def test_all_method_empty(self):
        result = self.storage.all()
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    def test_all_method_with_objects(self):
        # Add some test objects
        base_model = BaseModel()
        user = User()

        self.storage._FileStorage__objects["BaseModel.123"] = base_model
        self.storage._FileStorage__objects["User.456"] = user

        result = self.storage.all()
        self.assertEqual(len(result), 2)
        self.assertIn("BaseModel.123", result)
        self.assertIn("User.456", result)

    def test_new_method_base_model(self):
        obj = BaseModel()
        self.storage.new(obj)

        key = f"BaseModel.{obj.id}"
        self.assertIn(key, self.storage._FileStorage__objects)
        self.assertEqual(self.storage._FileStorage__objects[key], obj)

    def test_new_method_user(self):
        user = User()
        user.email = "test@example.com"
        user.password = "password123"
        self.storage.new(user)

        key = f"User.{user.id}"
        self.assertIn(key, self.storage._FileStorage__objects)
        self.assertEqual(self.storage._FileStorage__objects[key], user)

    def test_new_method_all_models(self):
        models = [
            BaseModel(),
            User(),
            State(),
            City(),
            Amenity(),
            Place(),
            Review()
        ]

        for model in models:
            self.storage.new(model)
            key = f"{model.__class__.__name__}.{model.id}"
            self.assertIn(key, self.storage._FileStorage__objects)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_method(self, mock_json_dump, mock_file):
        # Add test objects
        base_model = BaseModel()
        user = User()
        self.storage.new(base_model)
        self.storage.new(user)

        # Call save
        self.storage.save()

        # Verify file was opened for writing
        mock_file.assert_called_once_with(self.test_file, "w")

        # Verify json.dump was called
        mock_json_dump.assert_called_once()

        # Check the data structure passed to json.dump
        args, kwargs = mock_json_dump.call_args
        serialized_data = args[0]

        self.assertIsInstance(serialized_data, dict)
        self.assertEqual(len(serialized_data), 2)

        # Verify keys are in correct format
        base_key = f"BaseModel.{base_model.id}"
        user_key = f"User.{user.id}"
        self.assertIn(base_key, serialized_data)
        self.assertIn(user_key, serialized_data)

    @patch("builtins.open", new_callable=mock_open,
           read_data='{"BaseModel.123": {"__class__": "BaseModel", "id": "123", "created_at": "2023-01-01T00:00:00.000000", "updated_at": "2023-01-01T00:00:00.000000"}}')
    @patch("json.load")
    def test_reload_method_base_model(self, mock_json_load, mock_file):
        test_data = {
            "BaseModel.123": {
                "__class__": "BaseModel",
                "id": "123",
                "created_at": "2023-01-01T00:00:00.000000",
                "updated_at": "2023-01-01T00:00:00.000000"
            }
        }
        mock_json_load.return_value = test_data

        self.storage.reload()

        mock_file.assert_called_once_with(self.test_file, "r")
        mock_json_load.assert_called_once()

        # Verify object was recreated
        self.assertEqual(len(self.storage._FileStorage__objects), 1)
        self.assertIn("BaseModel.123", self.storage._FileStorage__objects)

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.load")
    def test_reload_method_all_models(self, mock_json_load, mock_file):
        test_data = {
            "BaseModel.1": {"__class__": "BaseModel", "id": "1"},
            "User.2": {"__class__": "User", "id": "2", "email": "test@test.com"},
            "State.3": {"__class__": "State", "id": "3", "name": "California"},
            "City.4": {"__class__": "City", "id": "4", "name": "San Francisco"},
            "Amenity.5": {"__class__": "Amenity", "id": "5", "name": "WiFi"},
            "Place.6": {"__class__": "Place", "id": "6", "name": "Cozy Apartment"},
            "Review.7": {"__class__": "Review", "id": "7", "text": "Great place!"}
        }
        mock_json_load.return_value = test_data

        self.storage.reload()

        # Verify all objects were recreated
        self.assertEqual(len(self.storage._FileStorage__objects), 7)
        for key in test_data.keys():
            self.assertIn(key, self.storage._FileStorage__objects)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_reload_method_file_not_found(self, mock_file):
        # Should not raise exception
        try:
            self.storage.reload()
        except FileNotFoundError:
            self.fail("reload() raised FileNotFoundError unexpectedly!")

        # Objects dictionary should remain empty
        self.assertEqual(len(self.storage._FileStorage__objects), 0)

    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    @patch("json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0))
    def test_reload_method_invalid_json(self, mock_json_load, mock_file):
        with self.assertRaises(json.JSONDecodeError):
            self.storage.reload()

    def test_save_and_reload_integration(self):
        base_model = BaseModel()
        user = User()
        user.email = "test@example.com"

        self.storage.new(base_model)
        self.storage.new(user)

        # Save to file
        self.storage.save()

        # Clear objects and reload
        self.storage._FileStorage__objects = {}
        self.storage.reload()

        # Verify objects were restored
        self.assertEqual(len(self.storage._FileStorage__objects), 2)

        base_key = f"BaseModel.{base_model.id}"
        user_key = f"User.{user.id}"
        self.assertIn(base_key, self.storage._FileStorage__objects)
        self.assertIn(user_key, self.storage._FileStorage__objects)

    def test_objects_persistence(self):
        user = User()
        user.email = "persist@test.com"
        user.password = "secret123"
        user.first_name = "John"
        user.last_name = "Doe"

        self.storage.new(user)
        self.storage.save()

        self.storage._FileStorage__objects = {}
        self.storage.reload()

        user_key = f"User.{user.id}"
        reloaded_user = self.storage._FileStorage__objects[user_key]

        self.assertEqual(reloaded_user.email, "persist@test.com")
        self.assertEqual(reloaded_user.password, "secret123")
        self.assertEqual(reloaded_user.first_name, "John")
        self.assertEqual(reloaded_user.last_name, "Doe")

    def test_multiple_operations(self):
        obj1 = BaseModel()
        self.storage.new(obj1)
        self.storage.save()

        obj2 = User()
        self.storage.new(obj2)
        self.storage.save()

        self.storage._FileStorage__objects = {}
        self.storage.reload()

        self.assertEqual(len(self.storage._FileStorage__objects), 2)

    def test_empty_save_and_reload(self):
        self.storage.save()
        self.storage.reload()
        self.assertEqual(len(self.storage._FileStorage__objects), 0)


if __name__ == '__main__':
    unittest.main()
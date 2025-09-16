#!/usr/bin/python3

import unittest
from unittest.mock import MagicMock
import uuid
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):

    def setUp(self):
        models.storage = MagicMock()

    def tearDown(self):
        pass

    def test_inheritance(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertIsInstance(amenity, Amenity)

    def test_attributes_exist(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'name'))

    def test_default_attribute_values(self):
        amenity = Amenity()
        self.assertEqual(amenity.name, "")

    def test_base_model_attributes(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'id'))
        self.assertTrue(hasattr(amenity, 'created_at'))
        self.assertTrue(hasattr(amenity, 'updated_at'))
        self.assertIsInstance(amenity.id, str)
        self.assertIsInstance(amenity.created_at, datetime)
        self.assertIsInstance(amenity.updated_at, datetime)

    def test_str_representation(self):
        amenity = Amenity()
        string_repr = str(amenity)
        self.assertIn("[Amenity]", string_repr)
        self.assertIn(f"({amenity.id})", string_repr)

    def test_to_dict(self):
        amenity = Amenity()
        amenity.name = "WiFi"

        amenity_dict = amenity.to_dict()

        self.assertEqual(amenity_dict['__class__'], 'Amenity')
        self.assertEqual(amenity_dict['name'], "WiFi")
        self.assertIn('id', amenity_dict)
        self.assertIn('created_at', amenity_dict)
        self.assertIn('updated_at', amenity_dict)

    def test_kwargs_initialization(self):
        kwargs = {
            "id": "test-id",
            "name": "Pool",
            "__class__": "Amenity"
        }

        amenity = Amenity(**kwargs)

        self.assertEqual(amenity.id, "test-id")
        self.assertEqual(amenity.name, "Pool")

    def test_attribute_assignment(self):
        amenity = Amenity()
        amenity.name = "Air Conditioning"

        self.assertEqual(amenity.name, "Air Conditioning")


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python3


import unittest
from unittest.mock import MagicMock
import uuid
from datetime import datetime
import models
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):

    def setUp(self):
        models.storage = MagicMock()

    def tearDown(self):
        pass

    def test_inheritance(self):
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertIsInstance(city, City)

    def test_attributes_exist(self):
        city = City()
        self.assertTrue(hasattr(city, 'state_id'))
        self.assertTrue(hasattr(city, 'name'))

    def test_default_attribute_values(self):
        city = City()
        self.assertEqual(city.state_id, "")
        self.assertEqual(city.name, "")

    def test_base_model_attributes(self):
        city = City()
        self.assertTrue(hasattr(city, 'id'))
        self.assertTrue(hasattr(city, 'created_at'))
        self.assertTrue(hasattr(city, 'updated_at'))
        self.assertIsInstance(city.id, str)
        self.assertIsInstance(city.created_at, datetime)
        self.assertIsInstance(city.updated_at, datetime)

    def test_str_representation(self):
        city = City()
        string_repr = str(city)
        self.assertIn("[City]", string_repr)
        self.assertIn(f"({city.id})", string_repr)

    def test_to_dict(self):
        city = City()
        city.state_id = "state-123"
        city.name = "San Francisco"

        city_dict = city.to_dict()

        self.assertEqual(city_dict['__class__'], 'City')
        self.assertEqual(city_dict['state_id'], "state-123")
        self.assertEqual(city_dict['name'], "San Francisco")
        self.assertIn('id', city_dict)
        self.assertIn('created_at', city_dict)
        self.assertIn('updated_at', city_dict)

    def test_kwargs_initialization(self):
        kwargs = {
            "id": "test-id",
            "state_id": "state-456",
            "name": "Los Angeles",
            "__class__": "City"
        }

        city = City(**kwargs)

        self.assertEqual(city.id, "test-id")
        self.assertEqual(city.state_id, "state-456")
        self.assertEqual(city.name, "Los Angeles")

    def test_attribute_assignment(self):
        city = City()
        city.state_id = "state-789"
        city.name = "New York City"

        self.assertEqual(city.state_id, "state-789")
        self.assertEqual(city.name, "New York City")


if __name__ == '__main__':
    unittest.main()

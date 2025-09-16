#!/usr/bin/python3

import unittest
from unittest.mock import MagicMock
import uuid
from datetime import datetime
import models
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):

    def setUp(self):
        models.storage = MagicMock()
        Place.amenity_ids = []

    def tearDown(self):
        pass

    def test_inheritance(self):
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertIsInstance(place, Place)

    def test_attributes_exist(self):
        place = Place()
        self.assertTrue(hasattr(place, 'city_id'))
        self.assertTrue(hasattr(place, 'user_id'))
        self.assertTrue(hasattr(place, 'name'))
        self.assertTrue(hasattr(place, 'description'))
        self.assertTrue(hasattr(place, 'number_rooms'))
        self.assertTrue(hasattr(place, 'number_bathrooms'))
        self.assertTrue(hasattr(place, 'max_guest'))
        self.assertTrue(hasattr(place, 'price_by_night'))
        self.assertTrue(hasattr(place, 'latitude'))
        self.assertTrue(hasattr(place, 'longitude'))
        self.assertTrue(hasattr(place, 'amenity_ids'))

    def test_default_attribute_values(self):
        place = Place()
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.name, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, [])

    def test_attribute_types(self):
        place = Place()
        self.assertIsInstance(place.city_id, str)
        self.assertIsInstance(place.user_id, str)
        self.assertIsInstance(place.name, str)
        self.assertIsInstance(place.description, str)
        self.assertIsInstance(place.number_rooms, int)
        self.assertIsInstance(place.number_bathrooms, int)
        self.assertIsInstance(place.max_guest, int)
        self.assertIsInstance(place.price_by_night, int)
        self.assertIsInstance(place.latitude, float)
        self.assertIsInstance(place.longitude, float)
        self.assertIsInstance(place.amenity_ids, list)

    def test_base_model_attributes(self):
        place = Place()
        self.assertTrue(hasattr(place, 'id'))
        self.assertTrue(hasattr(place, 'created_at'))
        self.assertTrue(hasattr(place, 'updated_at'))
        self.assertIsInstance(place.id, str)
        self.assertIsInstance(place.created_at, datetime)
        self.assertIsInstance(place.updated_at, datetime)

    def test_str_representation(self):
        place = Place()
        string_repr = str(place)
        self.assertIn("[Place]", string_repr)
        self.assertIn(f"({place.id})", string_repr)

    def test_to_dict(self):
        place = Place()
        place.city_id = "city-123"
        place.user_id = "user-456"
        place.name = "Cozy Apartment"
        place.description = "A nice place to stay"
        place.number_rooms = 2
        place.number_bathrooms = 1
        place.max_guest = 4
        place.price_by_night = 100
        place.latitude = 37.7749
        place.longitude = -122.4194
        place.amenity_ids = ["amenity1", "amenity2"]

        place_dict = place.to_dict()

        self.assertEqual(place_dict['__class__'], 'Place')
        self.assertEqual(place_dict['city_id'], "city-123")
        self.assertEqual(place_dict['user_id'], "user-456")
        self.assertEqual(place_dict['name'], "Cozy Apartment")
        self.assertEqual(place_dict['description'], "A nice place to stay")
        self.assertEqual(place_dict['number_rooms'], 2)
        self.assertEqual(place_dict['number_bathrooms'], 1)
        self.assertEqual(place_dict['max_guest'], 4)
        self.assertEqual(place_dict['price_by_night'], 100)
        self.assertEqual(place_dict['latitude'], 37.7749)
        self.assertEqual(place_dict['longitude'], -122.4194)
        self.assertEqual(place_dict['amenity_ids'], ["amenity1", "amenity2"])
        self.assertIn('id', place_dict)
        self.assertIn('created_at', place_dict)
        self.assertIn('updated_at', place_dict)

    def test_kwargs_initialization(self):
        kwargs = {
            "id": "test-id",
            "city_id": "city-789",
            "user_id": "user-101",
            "name": "Beach House",
            "description": "Beautiful beach house",
            "number_rooms": 3,
            "number_bathrooms": 2,
            "max_guest": 6,
            "price_by_night": 200,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "amenity_ids": ["pool", "wifi"],
            "__class__": "Place"
        }

        place = Place(**kwargs)

        self.assertEqual(place.id, "test-id")
        self.assertEqual(place.city_id, "city-789")
        self.assertEqual(place.user_id, "user-101")
        self.assertEqual(place.name, "Beach House")
        self.assertEqual(place.description, "Beautiful beach house")
        self.assertEqual(place.number_rooms, 3)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 6)
        self.assertEqual(place.price_by_night, 200)
        self.assertEqual(place.latitude, 34.0522)
        self.assertEqual(place.longitude, -118.2437)
        self.assertEqual(place.amenity_ids, ["pool", "wifi"])

    def test_attribute_assignment(self):
        place = Place()
        place.city_id = "new-city"
        place.user_id = "new-user"
        place.name = "Updated Place"
        place.description = "Updated description"
        place.number_rooms = 5
        place.number_bathrooms = 3
        place.max_guest = 10
        place.price_by_night = 300
        place.latitude = 40.7128
        place.longitude = -74.0060
        place.amenity_ids = ["gym", "spa", "wifi"]

        self.assertEqual(place.city_id, "new-city")
        self.assertEqual(place.user_id, "new-user")
        self.assertEqual(place.name, "Updated Place")
        self.assertEqual(place.description, "Updated description")
        self.assertEqual(place.number_rooms, 5)
        self.assertEqual(place.number_bathrooms, 3)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.latitude, 40.7128)
        self.assertEqual(place.longitude, -74.0060)
        self.assertEqual(place.amenity_ids, ["gym", "spa", "wifi"])

    def test_amenity_ids_list_operations(self):
        place = Place()

        place.amenity_ids.append("wifi")
        self.assertIn("wifi", place.amenity_ids)

        place.amenity_ids.extend(["pool", "gym"])
        self.assertEqual(len(place.amenity_ids), 3)
        self.assertIn("pool", place.amenity_ids)
        self.assertIn("gym", place.amenity_ids)


if __name__ == '__main__':
    unittest.main()

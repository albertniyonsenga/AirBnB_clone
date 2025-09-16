#!/usr/bin/python3

import unittest
from unittest.mock import MagicMock
import uuid
from datetime import datetime
import models
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):

    def setUp(self):
        models.storage = MagicMock()

    def tearDown(self):
        pass

    def test_inheritance(self):
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertIsInstance(user, User)

    def test_attributes_exist(self):
        user = User()
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))

    def test_default_attribute_values(self):
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_base_model_attributes(self):
        user = User()
        self.assertTrue(hasattr(user, 'id'))
        self.assertTrue(hasattr(user, 'created_at'))
        self.assertTrue(hasattr(user, 'updated_at'))
        self.assertIsInstance(user.id, str)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)

    def test_str_representation(self):
        user = User()
        string_repr = str(user)
        self.assertIn("[User]", string_repr)
        self.assertIn(f"({user.id})", string_repr)

    def test_to_dict(self):
        user = User()
        user.email = "test@example.com"
        user.first_name = "John"
        user.last_name = "Doe"

        user_dict = user.to_dict()

        self.assertEqual(user_dict['__class__'], 'User')
        self.assertEqual(user_dict['email'], "test@example.com")
        self.assertEqual(user_dict['first_name'], "John")
        self.assertEqual(user_dict['last_name'], "Doe")
        self.assertIn('id', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)

    def test_kwargs_initialization(self):
        kwargs = {
            "id": "test-id",
            "email": "test@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "__class__": "User"
        }

        user = User(**kwargs)

        self.assertEqual(user.id, "test-id")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Smith")

    def test_attribute_assignment(self):
        user = User()
        user.email = "new@example.com"
        user.password = "secret123"
        user.first_name = "Alice"
        user.last_name = "Johnson"

        self.assertEqual(user.email, "new@example.com")
        self.assertEqual(user.password, "secret123")
        self.assertEqual(user.first_name, "Alice")
        self.assertEqual(user.last_name, "Johnson")


if __name__ == '__main__':
    unittest.main()

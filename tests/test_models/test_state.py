#!/usr/bin/python3

import unittest
from unittest.mock import MagicMock
import uuid
from datetime import datetime
import models
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):

    def setUp(self):
        models.storage = MagicMock()

    def tearDown(self):
        pass

    def test_inheritance(self):
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertIsInstance(state, State)

    def test_attributes_exist(self):
        state = State()
        self.assertTrue(hasattr(state, 'name'))

    def test_default_attribute_values(self):
        state = State()
        self.assertEqual(state.name, "")

    def test_base_model_attributes(self):
        state = State()
        self.assertTrue(hasattr(state, 'id'))
        self.assertTrue(hasattr(state, 'created_at'))
        self.assertTrue(hasattr(state, 'updated_at'))
        self.assertIsInstance(state.id, str)
        self.assertIsInstance(state.created_at, datetime)
        self.assertIsInstance(state.updated_at, datetime)

    def test_str_representation(self):
        state = State()
        string_repr = str(state)
        self.assertIn("[State]", string_repr)
        self.assertIn(f"({state.id})", string_repr)

    def test_to_dict(self):
        state = State()
        state.name = "California"

        state_dict = state.to_dict()

        self.assertEqual(state_dict['__class__'], 'State')
        self.assertEqual(state_dict['name'], "California")
        self.assertIn('id', state_dict)
        self.assertIn('created_at', state_dict)
        self.assertIn('updated_at', state_dict)

    def test_kwargs_initialization(self):
        kwargs = {
            "id": "test-id",
            "name": "Texas",
            "__class__": "State"
        }

        state = State(**kwargs)

        self.assertEqual(state.id, "test-id")
        self.assertEqual(state.name, "Texas")

    def test_attribute_assignment(self):
        state = State()
        state.name = "New York"

        self.assertEqual(state.name, "New York")


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/python3

import unittest
from unittest.mock import patch, MagicMock
import uuid
from datetime import datetime
import time
import models
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        # Mock the storage
        models.storage = MagicMock()

    def tearDown(self):
        pass

    def test_init_no_kwargs(self):
        model = BaseModel()

        self.assertIsInstance(model.id, str)
        self.assertTrue(len(model.id) == 36)

        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

        self.assertEqual(model.created_at, model.updated_at)

        models.storage.new.assert_called_once_with(model)

    def test_init_with_kwargs(self):
        test_id = str(uuid.uuid4())
        test_created = datetime.now().isoformat()
        test_updated = datetime.now().isoformat()

        kwargs = {
            "id": test_id,
            "created_at": test_created,
            "updated_at": test_updated,
            "__class__": "BaseModel"
        }

        model = BaseModel(**kwargs)

        self.assertEqual(model.id, test_id)
        self.assertEqual(model.created_at, datetime.fromisoformat(test_created))
        self.assertEqual(model.updated_at, datetime.fromisoformat(test_updated))

        models.storage.new.assert_not_called()

    def test_init_with_kwargs_no_class_key(self):
        test_id = str(uuid.uuid4())

        kwargs = {
            "id": test_id,
            "custom_attr": "test_value"
        }

        model = BaseModel(**kwargs)

        self.assertEqual(model.id, test_id)
        self.assertEqual(model.custom_attr, "test_value")

        # Check that timestamps are created
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

        # Verify that storage.new() was called
        models.storage.new.assert_called_once_with(model)

    def test_init_datetime_conversion(self):
        test_created = "2023-10-10T10:10:10.123456"
        test_updated = "2023-10-10T11:11:11.654321"

        kwargs = {
            "created_at": test_created,
            "updated_at": test_updated,
            "__class__": "BaseModel"
        }

        model = BaseModel(**kwargs)

        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertEqual(model.created_at.isoformat(), test_created)
        self.assertEqual(model.updated_at.isoformat(), test_updated)

    def test_unique_ids(self):
        model1 = BaseModel()
        model2 = BaseModel()

        self.assertNotEqual(model1.id, model2.id)

    def test_str_representation(self):
        model = BaseModel()
        string_repr = str(model)

        # Check format: [ClassName] (id) {dict}
        self.assertIn("[BaseModel]", string_repr)
        self.assertIn(f"({model.id})", string_repr)
        self.assertIn(str(model.__dict__), string_repr)

    def test_save_method(self):
        model = BaseModel()
        original_updated_at = model.updated_at

        # Wait a small amount to ensure timestamp difference
        time.sleep(0.01)
        model.save()

        # Check that updated_at was changed
        self.assertNotEqual(model.updated_at, original_updated_at)
        self.assertGreater(model.updated_at, original_updated_at)

        # Verify that storage.save() was called
        models.storage.save.assert_called_once()

    def test_to_dict_method(self):
        model = BaseModel()
        model.name = "Test Model"
        model.number = 42

        model_dict = model.to_dict()

        # Check that dictionary contains all expected keys
        expected_keys = ['id', 'created_at', 'updated_at', '__class__', 'name', 'number']
        for key in expected_keys:
            self.assertIn(key, model_dict)

        # Check specific values
        self.assertEqual(model_dict['id'], model.id)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['name'], 'Test Model')
        self.assertEqual(model_dict['number'], 42)

        # Check that datetime objects are converted to ISO format strings
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertEqual(model_dict['created_at'], model.created_at.isoformat())
        self.assertEqual(model_dict['updated_at'], model.updated_at.isoformat())

    def test_to_dict_does_not_modify_original(self):
        model = BaseModel()
        original_dict = model.__dict__.copy()

        model_dict = model.to_dict()
        model_dict['new_key'] = 'new_value'

        # Check that original object wasn't modified
        self.assertEqual(model.__dict__, original_dict)
        self.assertNotIn('new_key', model.__dict__)

    # def test_kwargs_ignores_class_key(self):
    #     """Test that __class__ key is ignored in kwargs"""
    #     kwargs = {
    #         "id": "test-id",
    #         "__class__": "SomeOtherClass",
    #         "name": "test"
    #     }
    #
    #     model = BaseModel(**kwargs)
    #
    #     # Check that __class__ is not set as attribute
    #     self.assertFalse(hasattr(model, '__class__'))
    #     # But other attributes are set
    #     self.assertEqual(model.id, "test-id")
    #     self.assertEqual(model.name, "test")

    def test_inheritance_compatibility(self):
        class TestModel(BaseModel):
            pass

        test_model = TestModel()

        # Check that all BaseModel attributes are present
        self.assertIsInstance(test_model.id, str)
        self.assertIsInstance(test_model.created_at, datetime)
        self.assertIsInstance(test_model.updated_at, datetime)

        # Check string representation shows correct class name
        self.assertIn("[TestModel]", str(test_model))

        # Check to_dict shows correct class name
        model_dict = test_model.to_dict()
        self.assertEqual(model_dict['__class__'], 'TestModel')

    def test_edge_cases(self):
        # Test with empty kwargs
        model1 = BaseModel(**{})
        self.assertIsInstance(model1.id, str)
        self.assertIsInstance(model1.created_at, datetime)

        # Test with None values (should not cause errors)
        kwargs = {"custom_attr": None}
        model2 = BaseModel(**kwargs)
        self.assertIsNone(model2.custom_attr)

    @patch('uuid.uuid4')
    def test_uuid_generation(self, mock_uuid):
        mock_uuid.return_value = MagicMock()
        mock_uuid.return_value.__str__ = MagicMock(return_value="test-uuid")

        model = BaseModel()

        mock_uuid.assert_called_once()
        self.assertEqual(model.id, "test-uuid")

    @patch('models.base_model.datetime')
    def test_datetime_usage(self, mock_datetime):
        """Test that datetime.now() is called correctly"""
        test_time = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = test_time
        mock_datetime.fromisoformat = datetime.fromisoformat

        model = BaseModel()

        # Verify datetime.now() was called (for created_at)
        self.assertEqual(mock_datetime.now.call_count, 1)
        self.assertEqual(model.created_at, test_time)
        self.assertEqual(model.updated_at, test_time)


if __name__ == '__main__':
    unittest.main()

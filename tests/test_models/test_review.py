#!/usr/bin/python3

import unittest
from unittest.mock import MagicMock
import uuid
from datetime import datetime
import models
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    def setUp(self):
        models.storage = MagicMock()

    def tearDown(self):
        pass

    def test_inheritance(self):
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertIsInstance(review, Review)

    def test_attributes_exist(self):
        review = Review()
        self.assertTrue(hasattr(review, 'place_id'))
        self.assertTrue(hasattr(review, 'user_id'))
        self.assertTrue(hasattr(review, 'text'))

    def test_default_attribute_values(self):
        review = Review()
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")

    def test_base_model_attributes(self):
        review = Review()
        self.assertTrue(hasattr(review, 'id'))
        self.assertTrue(hasattr(review, 'created_at'))
        self.assertTrue(hasattr(review, 'updated_at'))
        self.assertIsInstance(review.id, str)
        self.assertIsInstance(review.created_at, datetime)
        self.assertIsInstance(review.updated_at, datetime)

    def test_str_representation(self):
        review = Review()
        string_repr = str(review)
        self.assertIn("[Review]", string_repr)
        self.assertIn(f"({review.id})", string_repr)

    def test_to_dict(self):
        review = Review()
        review.place_id = "place-123"
        review.user_id = "user-456"
        review.text = "Great place to stay!"

        review_dict = review.to_dict()

        self.assertEqual(review_dict['__class__'], 'Review')
        self.assertEqual(review_dict['place_id'], "place-123")
        self.assertEqual(review_dict['user_id'], "user-456")
        self.assertEqual(review_dict['text'], "Great place to stay!")
        self.assertIn('id', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)

    def test_kwargs_initialization(self):
        kwargs = {
            "id": "test-id",
            "place_id": "place-789",
            "user_id": "user-101",
            "text": "Amazing experience!",
            "__class__": "Review"
        }

        review = Review(**kwargs)

        self.assertEqual(review.id, "test-id")
        self.assertEqual(review.place_id, "place-789")
        self.assertEqual(review.user_id, "user-101")
        self.assertEqual(review.text, "Amazing experience!")

    def test_attribute_assignment(self):
        review = Review()
        review.place_id = "new-place"
        review.user_id = "new-user"
        review.text = "This is a detailed review of the place."

        self.assertEqual(review.place_id, "new-place")
        self.assertEqual(review.user_id, "new-user")
        self.assertEqual(review.text, "This is a detailed review of the place.")

    def test_long_text_review(self):
        review = Review()
        long_text = "This is a very long review. " * 50
        review.text = long_text

        self.assertEqual(review.text, long_text)
        self.assertIn(long_text, review.to_dict()['text'])


if __name__ == '__main__':
    unittest.main()

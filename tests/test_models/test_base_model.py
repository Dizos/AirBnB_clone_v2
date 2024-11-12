#!/usr/bin/python3
"""Unit tests for BaseModel class"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid
import time


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test cases"""
        self.model = BaseModel()

    def test_init(self):
        """Test initialization of BaseModel"""
        self.assertIsInstance(self.model, BaseModel)
        self.assertIsInstance(self.model.id, str)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_str(self):
        """Test string representation"""
        string = str(self.model)
        self.assertIn("[BaseModel]", string)
        self.assertIn(self.model.id, string)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.model.updated_at
        time.sleep(0.1)
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)

    def test_to_dict(self):
        """Test to_dict method"""
        model_dict = self.model.to_dict()
        
        # Test if all required keys are present
        self.assertIn('__class__', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIn('id', model_dict)
        
        # Test types of values
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertIsInstance(model_dict['id'], str)
        
        # Test datetime format
        datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
        try:
            datetime.strptime(model_dict['created_at'], datetime_format)
            datetime.strptime(model_dict['updated_at'], datetime_format)
        except ValueError:
            self.fail("Datetime string not in correct format")

    def test_attributes(self):
        """Test custom attribute assignment"""
        self.model.name = "My First Model"
        self.model.my_number = 89
        self.assertEqual(self.model.name, "My First Model")
        self.assertEqual(self.model.my_number, 89)

    def test_unique_id(self):
        """Test that each instance has a unique id"""
        model2 = BaseModel()
        self.assertNotEqual(self.model.id, model2.id)


if __name__ == '__main__':
    unittest.main()

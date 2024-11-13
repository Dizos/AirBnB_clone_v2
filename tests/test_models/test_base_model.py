#!/usr/bin/python3
"""
Unit tests for BaseModel class
"""
import os
import sys
import unittest
from datetime import datetime

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test cases"""
        self.model = BaseModel()
        self.model.name = "My_First_Model"
        self.model.my_number = 89

    def test_basic_init(self):
        """Test basic initialization with no arguments"""
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_kwargs_init(self):
        """Test initialization with kwargs"""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        
        # Test that all attributes are equal
        self.assertEqual(new_model.id, self.model.id)
        self.assertEqual(new_model.name, self.model.name)
        self.assertEqual(new_model.my_number, self.model.my_number)
        self.assertEqual(new_model.created_at, self.model.created_at)
        self.assertEqual(new_model.updated_at, self.model.updated_at)
        
        # Ensure they're different instances
        self.assertIsNot(new_model, self.model)

    def test_kwargs_init_datetime(self):
        """Test that datetime attributes are properly converted"""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)

    def test_kwargs_init_no_class(self):
        """Test that __class__ is not added as an attribute"""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertNotIn('__class__', new_model.__dict__)

    def test_str(self):
        """Test string representation"""
        string = str(self.model)
        self.assertIn("[BaseModel]", string)
        self.assertIn(self.model.id, string)

    def test_save(self):
        """Test save method"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(old_updated_at, self.model.updated_at)

    def test_to_dict(self):
        """Test to_dict method"""
        model_dict = self.model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertEqual(model_dict['id'], self.model.id)
        self.assertEqual(model_dict['name'], "My_First_Model")
        self.assertEqual(model_dict['my_number'], 89)

    def test_to_dict_datetime_format(self):
        """Test that datetime strings are in ISO format"""
        model_dict = self.model.to_dict()
        created_at = datetime.fromisoformat(model_dict['created_at'])
        updated_at = datetime.fromisoformat(model_dict['updated_at'])
        self.assertEqual(created_at, self.model.created_at)
        self.assertEqual(updated_at, self.model.updated_at)


if __name__ == '__main__':
    unittest.main()

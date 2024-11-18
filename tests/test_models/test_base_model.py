#!/usr/bin/python3
"""
Unit tests for BaseModel class
"""
import unittest
from datetime import datetime
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class"""

    def setUp(self):
        """Set up test cases"""
        self.model = BaseModel()
        self.model.name = "My_First_Model" 
        self.model.my_number = 89

    def test_init(self):
        """Test initialization"""
        self.assertIsInstance(self.model, BaseModel)
        self.assertTrue(hasattr(self.model, 'id'))
        self.assertTrue(hasattr(self.model, 'created_at'))
        self.assertTrue(hasattr(self.model, 'updated_at'))
        self.assertTrue(hasattr(self.model, 'name'))
        self.assertTrue(hasattr(self.model, 'my_number'))

    def test_init_from_dict(self):
        """Test initialization from dictionary"""
        model_json = self.model.to_dict()
        new_model = BaseModel(**model_json)
        
        self.assertEqual(self.model.id, new_model.id)
        self.assertEqual(self.model.created_at, new_model.created_at)
        self.assertEqual(self.model.updated_at, new_model.updated_at)
        self.assertEqual(self.model.name, new_model.name)
        self.assertEqual(self.model.my_number, new_model.my_number)
        self.assertFalse(hasattr(new_model, '__class__'))
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)
        self.assertFalse(self.model is new_model)

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
        self.assertEqual(model_dict['name'], 'My_First_Model')
        self.assertEqual(model_dict['my_number'], 89)
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertIsInstance(model_dict['id'], str)

if __name__ == '__main__':
    unittest.main()

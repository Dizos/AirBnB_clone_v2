#!/usr/bin/python3
"""Test module for console parameter creation"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place
import os


class TestConsoleCreate(unittest.TestCase):
    """Test cases for create command parameter handling"""

    def setUp(self):
        """Set up test cases"""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        storage.all().clear()

    def tearDown(self):
        """Clean up test cases"""
        if os.path.isfile("file.json"):
            os.remove("file.json")

    def test_create_state_with_name(self):
        """Test creating State with name parameter"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="California"')
        state_id = output.getvalue().strip()
        
        # Verify state was created with correct name
        state = storage.all()["State.{}".format(state_id)]
        self.assertEqual(state.name, "California")

    def test_create_state_with_escaped_quotes(self):
        """Test creating State with escaped quotes in name"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="Cal\"ifor\"nia"')
        state_id = output.getvalue().strip()
        
        state = storage.all()["State.{}".format(state_id)]
        self.assertEqual(state.name, 'Cal"ifor"nia')

    def test_create_state_with_underscore(self):
        """Test creating State with underscores in name"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="New_York_City"')
        state_id = output.getvalue().strip()
        
        state = storage.all()["State.{}".format(state_id)]
        self.assertEqual(state.name, "New York City")

    def test_create_place_with_multiple_params(self):
        """Test creating Place with multiple parameter types"""
        command = ('create Place city_id="0001" user_id="0001" '
                  'name="My_little_house" number_rooms=4 number_bathrooms=2 '
                  'max_guest=10 price_by_night=300 latitude=37.773972 '
                  'longitude=-122.431297')
        
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd(command)
        place_id = output.getvalue().strip()
        
        place = storage.all()["Place.{}".format(place_id)]
        # Verify string parameters
        self.assertEqual(place.city_id, "0001")
        self.assertEqual(place.user_id, "0001")
        self.assertEqual(place.name, "My little house")
        
        # Verify integer parameters
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        
        # Verify float parameters
        self.assertEqual(place.latitude, 37.773972)
        self.assertEqual(place.longitude, -122.431297)

    def test_create_with_invalid_parameters(self):
        """Test creating object with invalid parameters"""
        # Invalid integer
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create Place number_rooms=NotANumber')
        place_id = output.getvalue().strip()
        
        place = storage.all()["Place.{}".format(place_id)]
        self.assertFalse(hasattr(place, 'number_rooms'))

        # Invalid float
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create Place latitude=NotAFloat')
        place_id = output.getvalue().strip()
        
        place = storage.all()["Place.{}".format(place_id)]
        self.assertFalse(hasattr(place, 'latitude'))

    def test_create_with_malformed_parameters(self):
        """Test creating object with malformed parameters"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name=California')  # No quotes
        state_id = output.getvalue().strip()
        
        state = storage.all()["State.{}".format(state_id)]
        self.assertFalse(hasattr(state, 'name'))


if __name__ == '__main__':
    unittest.main()

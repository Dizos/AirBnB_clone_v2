#!/usr/bin/python3
"""
Test module for testing console database operations
"""
import unittest
import MySQLdb
import os
from os import getenv
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand


class TestConsoleDB(unittest.TestCase):
    """Test cases for console commands with database storage"""

    @classmethod
    def setUpClass(cls):
        """Set up test database connection"""
        cls.conn = MySQLdb.connect(
            host=getenv('HBNB_MYSQL_HOST', 'localhost'),
            user=getenv('HBNB_MYSQL_USER', 'hbnb_test'),
            passwd=getenv('HBNB_MYSQL_PWD', 'hbnb_test_pwd'),
            db=getenv('HBNB_MYSQL_DB', 'hbnb_test_db')
        )
        cls.cursor = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        """Clean up database connection"""
        cls.cursor.close()
        cls.conn.close()

    def setUp(self):
        """Set up for each test"""
        # Clean up states table before each test
        self.cursor.execute("DELETE FROM states")
        self.conn.commit()

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                    "This test only works with db storage")
    def test_create_state(self):
        """Test that create State command adds a record to states table"""
        # Get initial count of states
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Execute console command
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="California"')

        # Get new count of states
        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchone()[0]

        # Verify one record was added
        self.assertEqual(new_count, initial_count + 1)

        # Verify the state name was correctly saved
        self.cursor.execute("SELECT name FROM states ORDER BY id DESC LIMIT 1")
        state_name = self.cursor.fetchone()[0]
        self.assertEqual(state_name, "California")

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                    "This test only works with db storage")
    def test_create_state_multiple(self):
        """Test creating multiple states"""
        states = ["California", "Arizona", "Texas"]
        
        # Get initial count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Create multiple states
        for state in states:
            with patch('sys.stdout', new=StringIO()) as output:
                HBNBCommand().onecmd(f'create State name="{state}"')

        # Get new count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchone()[0]

        # Verify records were added
        self.assertEqual(new_count, initial_count + len(states))

        # Verify state names were saved correctly
        self.cursor.execute("SELECT name FROM states ORDER BY id DESC LIMIT 3")
        saved_states = [row[0] for row in self.cursor.fetchall()]
        self.assertEqual(sorted(saved_states), sorted(states))

    @unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
                    "This test only works with db storage")
    def test_create_state_invalid(self):
        """Test creating state with invalid name"""
        # Get initial count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Try to create state with empty name
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name=""')

        # Get new count
        self.cursor.execute("SELECT COUNT(*) FROM states")
        new_count = self.cursor.fetchone()[0]

        # Verify no record was added
        self.assertEqual(new_count, initial_count)

if __name__ == "__main__":
    unittest.main()

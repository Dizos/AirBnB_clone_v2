#!/usr/bin/python3
"""Module for Base class
Contains the Base class for the AirBnB clone console.
"""
import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models"""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes
        
        Args:
            *args: Variable length argument list (not used)
            **kwargs: Arbitrary keyword arguments
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        # Convert string to datetime object
                        setattr(self, key, datetime.fromisoformat(value))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns string representation of instance"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Returns dictionary containing all keys/values of __dict__"""
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        dict_copy['created_at'] = self.created_at.isoformat()
        dict_copy['updated_at'] = self.updated_at.isoformat()
        return dict_copy

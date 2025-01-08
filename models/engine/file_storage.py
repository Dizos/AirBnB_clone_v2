#!/usr/bin/python3
"""
This module defines the FileStorage class which handles storage
of objects in JSON format.
"""
import json
from os.path import exists


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances.
    Handles persistent storage of all class instances.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of stored objects.
        If cls is specified, returns only objects of that class.

        Args:
            cls (class, optional): Class to filter objects by. Defaults to None.

        Returns:
            dict: Dictionary of stored objects, filtered by class if specified.
        """
        if cls is None:
            return self.__objects
        
        filtered_dict = {}
        for key, value in self.__objects.items():
            if isinstance(value, cls):
                filtered_dict[key] = value
        return filtered_dict

    def new(self, obj):
        """
        Adds new object to storage dictionary.
        
        Args:
            obj: Object to add to storage.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file.
        Saves storage dictionary to file.
        """
        serialized = {}
        for key, obj in self.__objects.items():
            serialized[key] = obj.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(serialized, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        Only if the JSON file exists; otherwise, do nothing.
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
        }

        if exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value["__class__"]
                    self.__objects[key] = classes[class_name](**value)

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside.
        
        Args:
            obj: Object to delete from storage. If None, do nothing.
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

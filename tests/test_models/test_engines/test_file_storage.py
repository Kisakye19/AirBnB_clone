#!/usr/bin/python3
"""
Unittest for FileStorage class
"""

import unittest
import os
from models import storage
from models.base_model import BaseModel
from models.user import User

class TestFileStorage(unittest.TestCase):
    """Defines tests for FileStorage class"""

    def test_instance(self):
        """Test instantiation of FileStorage class"""
        self.assertIsInstance(storage, FileStorage)

    def test_file_path(self):
        """Test if file_path is a string"""
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def test_objects(self):
        """Test if __objects is a dictionary"""
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_all(self):
        """Test the all() method of FileStorage class"""
        obj_dict = storage.all()
        self.assertIsInstance(obj_dict, dict)
        self.assertIs(obj_dict, FileStorage._FileStorage__objects)

    def test_new(self):
        """Test the new() method of FileStorage class"""
        user = User()
        storage.new(user)
        key = "{}.{}".format(user.__class__.__name__, user.id)
        self.assertIsNotNone(FileStorage._FileStorage__objects[key])
        self.assertIs(FileStorage._FileStorage__objects[key], user)

    def test_save_reload(self):
        """Test the save() and reload() methods of FileStorage class"""
        user = User()
        user.name = "John"
        user.save()
        key = "{}.{}".format(user.__class__.__name__, user.id)
        user_copy = storage.all()[key].to_dict()
        storage.reload()
        self.assertTrue(os.path.exists("file.json"))
        self.assertIsInstance(storage.all(), dict)
        self.assertIn(key, storage.all())
        self.assertDictEqual(storage.all()[key].to_dict(), user_copy)

if __name__ == "__main__":
    unittest.main()


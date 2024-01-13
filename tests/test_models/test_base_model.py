#!/usr/bin/python3
"""
Module for testing the BaseModel class
"""

import unittest
from models.base_model import BaseModel
from datetime import datetime

class TestBaseModel(unittest.TestCase):
    """
    Test cases for the BaseModel class
    """

    def test_attributes(self):
        """
        Test the public instance attributes of BaseModel
        """
        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89

        self.assertEqual(type(my_model.id), str)
        self.assertEqual(type(my_model.created_at), datetime)
        self.assertEqual(type(my_model.updated_at), datetime)

    def test_str_method(self):
        """
        Test the __str__ method of BaseModel
        """
        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89

        expected_str = "[BaseModel] ({}) {}".format(my_model.id, my_model.__dict__)
        self.assertEqual(str(my_model), expected_str)

    def test_save_method(self):
        """
        Test the save method of BaseModel
        """
        my_model = BaseModel()
        updated_at_before_save = my_model.updated_at
        my_model.save()

        self.assertNotEqual(updated_at_before_save, my_model.updated_at)

    def test_to_dict_method(self):
        """
        Test the to_dict method of BaseModel
        """
        my_model = BaseModel()
        my_model.name = "My First Model"
        my_model.my_number = 89
        my_model_dict = my_model.to_dict()

        self.assertEqual(type(my_model_dict["id"]), str)
        self.assertEqual(type(my_model_dict["created_at"]), str)
        self.assertEqual(type(my_model_dict["updated_at"]), str)
        self.assertEqual(type(my_model_dict["__class__"]), str)
        self.assertEqual(type(my_model_dict["my_number"]), int)
        self.assertEqual(type(my_model_dict["name"]), str)


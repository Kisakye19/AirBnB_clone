#!/usr/bin/python3
"""
Module that defines the BaseModel class
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """
    Defines the base model for other classes in the project
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        Returns a string representation of the object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()  # as instructed also in task 5

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__ of the instance
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict


#!/usr/bin/python3
"""
Module for FileStorage class
"""
import json
from os.path import exists
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}
    
    class_dict = {
    "BaseModel": BaseModel,
    "User": User,
    "Place": Place,
    "Amenity": Amenity,
    "City": City,
    "Review": Review,
    "State": State
    }

    def all(self):
        """Returns the dictionary __objects"""
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        new_dict = []
        for obj in self.__objects.values():
            new_dict.append(obj.to_dict())
        with open(self.__file_path, "w", encoding='utf-8') as file:
            json.dump(new_dict, file)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, "r", encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    class_name, obj_id = item["__class__"], item["id"]
                    cls = storage.class_dict[class_name]
                    obj = cls(**item)
                    key = "{}.{}".format(class_name, obj_id)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass
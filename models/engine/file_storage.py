#!/usr/bin/python3

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as file:
            json.dump(new_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects."""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for key, value in data.items():
                cls_name, obj_id = key.split('.')
                class_dict = eval(cls_name).__dict__.copy()
                del class_dict['__class__']
                del class_dict['__module__']
                del class_dict['created_at']
                del class_dict['updated_at']
                for k, v in value.items():
                    if k in class_dict:
                        if isinstance(class_dict[k], str):
                            value[k] = str(value[k])
                        elif isinstance(class_dict[k], int):
                            value[k] = int(value[k])
                        elif isinstance(class_dict[k], float):
                            value[k] = float(value[k])
                instance = eval(cls_name)(**value)
                FileStorage.__objects[key] = instance
        except FileNotFoundError:
            pass

storage = FileStorage()
storage.reload()

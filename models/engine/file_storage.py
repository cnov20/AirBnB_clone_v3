#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""
import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime
from models import storage

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """handles long term storage of all class instances"""
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    """CNC - this variable is a dictionary with:
    keys: Class Names
    values: Class type (used for instantiation)
    """
    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """returns private attribute: __objects"""
        if cls:
            objects_dict = {}
            for class_id, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    objects_dict[class_id] = obj
            return objects_dict
        return FileStorage.__objects

    def new(self, obj):
        """sets / updates in __objects the obj with key <obj class name>.id"""
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        fname = FileStorage.__file_path
        d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            d[bm_id] = bm_obj.to_json()
        with open(fname, mode='w', encoding='utf-8') as f_io:
            json.dump(d, f_io)

    def reload(self):
        """if file exists, deserializes JSON file to __objects, else nothing"""
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """ deletes obj from __objects if it's inside """
        try:
            del __objects[obj]
        except:
            return

    def close(self):
        """
            calls the reload() method for deserialization from JSON to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        A method to retrieve one object.
        Returns the object based on the class name
        and its ID, or None if not found
        """
        for i, j in storage.all().items():
            m = i.split('.')
            if (m[0] == cls and m[1] == id):
                return j


    def count(self, cls=None):
        """
        method to count the number of objects in storage
        Returns the number of objects in storage matching the given
        class name. If no name is passed, returns the count of
        all objects in storage.
        """
        if cls == None:
            return len((storage.all()))
        else:
            return len((storage.all(cls)))

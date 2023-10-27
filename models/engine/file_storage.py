#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""
import json
from models import base_model, amenity, city, place, review, state, user


class FileStorage:
    """
    Handles long-term storage of all class instances.
    """
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary of all objects.
        """
        if cls is not None:
            new_objs = {}
            for clsid, obj in self.__objects.items():
                if type(obj).__name__ == cls:
                    new_objs[clsid] = obj
            return new_objs
        else:
            return self.__objects

    def new(self, obj):
        """
        Sets or updates the object in __objects using the key <obj class name>.id.
        """
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[bm_id] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        fname = self.__file_path
        storage_d = {}
        for bm_id, bm_obj in self.__objects.items():
            storage_d[bm_id] = bm_obj.to_json(saving_file_storage=True)
        with open(fname, mode='w', encoding='utf-8') as f_io:
            json.dump(storage_d, f_io)

    def reload(self):
        """
        Deserializes the JSON file to __objects if the file exists.
        """
        fname = self.__file_path
        self.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except FileNotFoundError:
            return
        for o_id, d in new_objs.items():
            k_cls = d['__class__']
            self.__objects[o_id] = self.CNC[k_cls](**d)

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it exists.
        """
        if obj:
            obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
            all_class_objs = self.all(obj.__class__.__name__)
            if all_class_objs.get(obj_ref):
                del self.__objects[obj_ref]
            self.save()

    def delete_all(self):
        """
        Deletes all stored objects for testing purposes.
        """
        try:
            with open(self.__file_path, mode='w'):
                pass
        except FileNotFoundError:
            pass
        self.__objects = {}
        self.save()

    def close(self):
        """
        Calls the reload() method for deserialization from JSON to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves one object based on class name and id.
        """
        if cls and id:
            fetch_obj = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch_obj)
        return None

    def count(self, cls=None):
        """
        Returns the count of all objects in storage.
        """
        return len(self.all(cls))

#!/usr/bin/python3
"""
    The Base_Module!
"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        '''Initializes instance attributes'''

        if len(kwargs) == 0:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            for key in kwargs.keys():
                """
                    check and escape the __class__ key
                """
                if key == "__class__":
                    continue
                else:
                    """
                        check and change the format for updated_at & created_at
                    """
                    if key == "updated_at" or key == "created_at":
                        kwargs[key] = datetime.strptime(
                            kwargs[key], "%Y-%m-%dT%H:%M:%S.%f")
                    # set the attributes of the instance
                    setattr(self, key, kwargs[key])

    def __str__(self):
        """
            Then return string representation of the Model
        """
        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """
            to update time of the model
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
            the custom representation of a model
        """
        custom_dict = {}
        for key in self.__dict__.keys():
            if key not in ('created_at', 'updated_at'):
                custom_dict[key] = self.__dict__[key]
            else:
                custom_dict[key] = datetime.isoformat(
                    self.__dict__[key])
        custom_dict['__class__'] = self.__class__.__name__
        return (custom_dict)

    def delete(self):
        """
            To delete the current instance from storage
        """
        k = "{}.{}".format(type(self).__name__, self.id)
        del models.storage.__objects[k]

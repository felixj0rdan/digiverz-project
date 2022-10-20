import datetime
from bson.objectid import ObjectId

from db import db


class UserModel:

    email = None
    password = None
    active = True
    date_time = str(datetime.datetime.now())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __writeJson(self):
        return {
            # "id": self._id,
            "email": self.email,
            "password": self.password,
            "active": self.active,
            "date_time": str(self.date_time),
        }

    @classmethod
    def res_json(cls, user):
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "active": user["active"],
            "date_time": str(user["date_time"]),
        }

    def add_to_db(self):
        db.users.insert_one(self.__writeJson())

    @classmethod
    def find_one_by_email(cls, email):
        return db.users.find_one({"email": email})

    @classmethod
    def find_by_id(cls, id):
        return db.users.find_one({"_id": id})

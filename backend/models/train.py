import datetime
from bson.objectid import ObjectId

from db import db


class TrainingFileModel:

    file_path = None
    user_id = None
    date_time = str(datetime.datetime.now())

    def __init__(self, user_id, file_path):
        self.user_id = user_id
        self.file_path = file_path

    def __writeJson(self):
        return {
            # "id": self._id,
            "file_path": self.file_path,
            "user_id": self.user_id,
            "date_time": str(self.date_time),
        }

    @classmethod
    def res_json(cls, file):
        return {
            "id": str(file["_id"]),
            "user_id": file["user_id"],
            "file_path": file["file_path"],
            "date_time": str(file["date_time"]),
        }

    def add_to_db(self):
        db.file.insert_one(self.__writeJson())

    @classmethod
    def find_one_by_id(cls, id):
        return db.file.find_one({"_id": id})

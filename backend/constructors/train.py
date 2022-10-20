from flask_restful import Resource, reqparse
from flask import jsonify
import json
from flask import (
    request,
    jsonify,
    send_file,
    send_from_directory,
    url_for,
    redirect,
    render_template,
)
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
import os
import pandas as pd

from models.train import TrainingFileModel
from models.user import UserModel

ASSETS_FOLDER = "assets"
ALLOWED_EXTENSIONS = set(["csv", "xls", "xlsx"])


class UploadCSV(Resource):
    @jwt_required
    def post(self):

        if "file" not in request.files:
            return {"message": "No file uploaded!"}, 404

        files = request.files.getlist("file")
        errors = {}
        for file in files:
            # print("check")
            if (
                file
                and "." in file.filename
                and file.filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
            ):
                user_id = get_jwt_identity()

                user = UserModel.find_by_id(user_id)

                filename = secure_filename(file.filename)

                URL = request.url_root[:-1]
                FILE = str(user_id) + "-" + filename

                file.save(os.path.join(ASSETS_FOLDER, FILE))

                training_file = TrainingFileModel(
                    user_id, URL + "/api/training-file/" + FILE
                )

                training_file.add_to_db()
                success = True

                return {"message": "success", "link": training_file.file_path}

            else:
                return {"message": "error"}


# class TrainModel(Resource):


# class TrainingFile(Resource):
# def get(self, path):
#     print(path)
#     try:
#         # if os.path.isfile(ASSETS_FOLDER + path):
#         #     return send_file(ASSETS_FOLDER + path)
#         # return send_file(ASSETS_FOLDER + "/" + path)
#         data = pd.read_csv(ASSETS_FOLDER + "/" + path)
#         return render_template("table.html", tables=[data.to_html()], titles=[""])
#     except FileNotFoundError:
#         return {"message": "File not Found"}, 404

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
import flask_excel as excel
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sktime.forecasting.model_selection import temporal_train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from datetime import date, timedelta, datetime

from models.mlmodel import TrainingFileModel
from models.user import UserModel


ASSETS_FOLDER = "assets"
ALLOWED_EXTENSIONS = set(["csv", "xls", "xlsx"])


class Predict(Resource):
    @jwt_required
    def post(self):
        # print(request.values)
        # data = dict(request.form)
        print("data")

        if not request.files.getlist("file")[0]:
            print("check123")
            return {"message": "No file uploaded!"}, 404

        print("Check")
        file = request.files.getlist("file")[0]
        # print(request.files.getlist("file[]"))
        errors = {}
        # for file in files:
        print("check585")

        def create_feature(df):

            df = df.copy()
            df["dayofweek"] = df.index.dayofweek
            df["month"] = df.index.month
            df["year"] = df.index.year
            df["dayofyear"] = df.index.dayofyear
            return df

        if (
            file
            and "." in file.filename
            and file.filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        ):
            user_id = get_jwt_identity()  # ignore

            user = UserModel.find_by_id(user_id)  # ignore

            filename = secure_filename(file.filename)

            URL = request.url_root[:-1]
            FILE = str(user_id) + "-" + filename

            file.save(os.path.join(ASSETS_FOLDER + "/train/", FILE))

            training_file = TrainingFileModel(
                user_id, URL + "/api/training-file/" + FILE
            )

            training_file.add_to_db()  # ignore
            success = True

            # D:\kaar-projects\digiverz-project\backend\assets\634d20b43135995401986e22-train.csv

            df = pd.read_csv("assets/train/" + FILE)

            df["Date"] = pd.to_datetime(df["Date"])
            df.sort_values(by="Date", inplace=True)
            df = df.groupby(pd.Grouper(key="Date", freq="D")).sum()
            print(df.tail())

            train, test = temporal_train_test_split(df, test_size=0.25)

            train = create_feature(train)
            test = create_feature(test)

            # FEATURES = ["dayofweek", "month", "year", "dayofyear"]
            FEATURES = ["dayofyear"]
            TARGET = "Sales"

            X_train = train[FEATURES]
            y_train = train[TARGET]

            X_test = test[FEATURES]
            y_test = test[TARGET]

            reg = xgb.XGBRegressor(
                n_estimators=1000, early_stopping_rounds=50, learning_rate=0.01
            )
            reg.fit(
                X_train,
                y_train,
                eval_set=[(X_train, y_train), (X_test, y_test)],
                verbose=50,
            )

            test["pred"] = reg.predict(X_test)
            df = df.merge(test[["pred"]], how="left", left_index=True, right_index=True)

            x = mean_squared_error(test["Sales"], test["pred"], squared=False)
            print(x)

            days = int(request.form.get("days"))

            # count = 600
            start_date = df.index[-1]
            # print(X_test.tail())
            # print(df.index[-1])
            pred_df = pd.DataFrame(
                {
                    "Date": [
                        single_date
                        for single_date in (
                            start_date + timedelta(n) for n in range(1, days + 1)
                        )
                    ]
                }
            )
            # pred_df.set_index = pd.to_datetime(pred_df["Date"])

            pred_df["Date"] = pd.to_datetime(pred_df["Date"])
            pred_df = pred_df.groupby(pd.Grouper(key="Date", freq="D")).sum()
            pred_df = create_feature(pred_df)
            X_pred_df = pred_df[FEATURES]

            res = pd.DataFrame()

            pred_df["Sales"] = reg.predict(X_pred_df)

            # print(pred_df.head())

            # pred_df["pred"].plot(ax=ax, label="res")

            # plt.show()
            print(pred_df)
            PRED_FILE = str(user_id) + "-pred-for-" + filename
            pred_df.to_csv(ASSETS_FOLDER + "/predicted/" + PRED_FILE)
            pred_file_url = URL + "/api/prediction-file/" + PRED_FILE

            return {
                "message": "success",
                "view_train_file": training_file.file_path,
                "pred_file_url": pred_file_url,
                "pred_data": {
                    "datetime": list(pred_df.index.strftime("%d-%m-%y")),
                    "Sales": list(pred_df["Sales"]),
                },
                "train_data": {
                    "datetime": list(df.index.strftime("%d-%m-%y")),
                    "Sales": list(df["Sales"]),
                },
            }

        else:
            return {"message": "error"}


class PredictionFile(Resource):
    def get(self, path):
        print(path)
        try:
            return send_from_directory(
                ASSETS_FOLDER + "/predicted/",
                path=path,
                as_attachment=True,
                mimetype="text/csv",
            )

        except FileNotFoundError:
            return {"message": "File not Found"}, 404

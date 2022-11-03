from flask_restful import Resource
from flask import request, send_from_directory
from werkzeug.utils import secure_filename
from flask_jwt_extended import get_jwt_identity, jwt_required
import os

import pandas as pd
import numpy as np
from sktime.forecasting.model_selection import temporal_train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from datetime import date, timedelta, datetime

from models.mlmodel import TrainingFileModel
from models.user import UserModel


ASSETS_FOLDER = "assets"
ALLOWED_EXTENSIONS = set(["csv", "xls", "xlsx"])


class Predict(Resource):
    # @jwt_required
    def post(self):

        if not request.files.getlist("file")[0]:
            return {"message": "No file uploaded!"}, 404

        file = request.files.getlist("file")[0]
        duration = int(request.form.get("duration"))
        periodicity = request.form.get("periodicity")
        days = 0
        freq = ""
        datetimeFormat = ""

        if periodicity == "months":
            days = int(duration) * 28
            freq = "M"
            datetimeFormat = "%b-%y"
        elif periodicity == "weeks":
            days = int(duration) * 7
            freq = "W"
            datetimeFormat = "Week %W, %y"
        else:
            days = int(duration)
            freq = "D"
            datetimeFormat = "%d-%m-%y"

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
            user_id = get_jwt_identity()

            user = UserModel.find_by_id(user_id)

            filename = secure_filename(file.filename)

            URL = request.url_root[:-1]
            FILE = "file" + "-" + filename

            file.save(os.path.join(ASSETS_FOLDER + "/train/", FILE))

            training_file = TrainingFileModel(
                user_id, URL + "/api/training-file/" + FILE
            )

            training_file.add_to_db()

            df = pd.read_csv("assets/train/" + FILE)

            df["Date"] = pd.to_datetime(df["Date"])
            df.sort_values(by="Date", inplace=True)
            df = df.groupby(pd.Grouper(key="Date", freq=freq)).sum()  #

            train, test = temporal_train_test_split(df, test_size=0.25)

            train = create_feature(train)
            test = create_feature(test)

            FEATURES = ["dayofyear", "month", "dayofweek"]
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
            test["error"] = np.abs(test[TARGET] - test["pred"])

            rmse = mean_squared_error(test["Sales"], test["pred"], squared=False)

            start_date = df.index[-1]
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

            pred_df["Date"] = pd.to_datetime(pred_df["Date"])
            pred_df = pred_df.groupby(pd.Grouper(key="Date", freq=freq)).sum()  #
            pred_df = create_feature(pred_df)
            X_pred_df = pred_df[FEATURES]

            res = pd.DataFrame()

            pred_df["Sales"] = reg.predict(X_pred_df)

            pred_df.reset_index(inplace=True)
            pred_df = pred_df.groupby(pd.Grouper(key="Date", freq=freq)).sum()
            pred_df.sort_values(by="Date", inplace=True)
            pred_df.index = pred_df.index.strftime(datetimeFormat)
            pred_df.reset_index(inplace=True)

            df.reset_index(inplace=True)
            df = df.groupby(pd.Grouper(key="Date", freq=freq)).sum()
            df.sort_values(by="Date", inplace=True)
            df.index = df.index.strftime(datetimeFormat)
            df.reset_index(inplace=True)

            test.reset_index(inplace=True)
            test = test.groupby(pd.Grouper(key="Date", freq=freq)).sum()
            test.sort_values(by="Date", inplace=True)
            test.index = test.index.strftime(datetimeFormat)
            test.reset_index(inplace=True)

            PRED_FILE = "predicted-" + filename
            pred_df.to_csv(ASSETS_FOLDER + "/predicted/" + PRED_FILE)
            pred_file_url = URL + "/api/predicted/" + PRED_FILE

            ERR_FILE = "error-" + filename
            test.to_csv(ASSETS_FOLDER + "/error/" + ERR_FILE)
            err_file_url = URL + "/api/error/" + ERR_FILE
            print(err_file_url)

            return {
                "message": "success",
                "view_train_file": training_file.file_path,
                "pred_file_url": pred_file_url,
                "error_file_url": err_file_url,
                "rmse": "{0:.2f}".format(rmse),
                "duration": duration,
                "periodicity": periodicity,
                "error_data": {
                    "datetime": list(test["Date"]),
                    "error": list(test["error"]),
                },
                "pred_data": {
                    "datetime": list(pred_df["Date"]),
                    "Sales": list(pred_df["Sales"]),
                },
                "train_data": {
                    "datetime": list(df["Date"]),
                    "Sales": list(df["Sales"]),
                },
                "x": list(df["Date"]) + list(pred_df["Date"]),
            }

        else:
            return {"message": "error"}


class PredictionFile(Resource):
    def get(self, path):
        try:
            return send_from_directory(
                ASSETS_FOLDER + "/predicted/",
                path=path,
                as_attachment=True,
                mimetype="text/csv",
            )

        except FileNotFoundError:
            return {"message": "File not Found"}, 404


class ErrorFile(Resource):
    def get(self, path):
        try:
            return send_from_directory(
                ASSETS_FOLDER + "/error/",
                path=path,
                as_attachment=True,
                mimetype="text/csv",
            )

        except FileNotFoundError:
            return {"message": "File not Found"}, 404

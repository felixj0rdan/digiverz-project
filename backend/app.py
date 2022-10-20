from flask import Flask, jsonify, request, redirect, render_template, url_for
from flask_pymongo import PyMongo, pymongo
from flask_restful import Api
from flask_jwt_extended import JWTManager
import pandas as pd

from blacklist import BLACKLIST
from constructors.user import UserSignup, UserLogin, UserLogout, TokenRefresh
from constructors.train import UploadCSV

ASSETS_FOLDER = "assets"

app = Flask(__name__)
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
api = Api(app)
app.secret_key = "felix"
jwt = JWTManager(app)


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # Here we blacklist particular JWTs that have been created in the past.
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(UserSignup, "/api/signup")
api.add_resource(UserLogin, "/api/login")
api.add_resource(UserLogout, "/api/logout")
api.add_resource(TokenRefresh, "/api/refresh")
api.add_resource(UploadCSV, "/api/train")


@app.route("/api/training-file/<string:path>")
def getFile(path):
    print(path)
    try:
        data = pd.read_csv(ASSETS_FOLDER + "/" + path, nrows=50)
        return render_template("table.html", tables=[data.to_html()], titles=[""])

    except FileNotFoundError:
        return {"message": "File not Found"}, 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)

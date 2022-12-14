from flask_restful import Resource, reqparse
import json
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)

from blacklist import BLACKLIST
from models.user import UserModel


class UserSignup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="This field cannot be left blank!"
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be left blank!"
    )

    def post(self):
        data = UserSignup.parser.parse_args()

        if UserModel.find_one_by_email(data["email"]):
            return {"message": "User already exists."}, 400

        user = UserModel(**data)

        user.add_to_db()

        return {"message": "User created"}, 200


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "email", type=str, required=True, help="This field cannot be blank."
        )
        parser.add_argument(
            "password", type=str, required=True, help="This field cannot be blank."
        )
        data = parser.parse_args()

        user = UserModel.find_one_by_email(data["email"])

        # this is what the `authenticate()` function did in security.py
        if user:
            if safe_str_cmp(user["password"], data["password"]):

                access_token = create_access_token(
                    identity=str(user["_id"]), fresh=True
                )
                refresh_token = create_refresh_token(str(user["_id"]))
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user_id": str(user["_id"]),
                    "email": user["email"],
                }, 200
            return {"message": "Invalid Credentials!"}, 401
        return {"message": "User not found!", "status": 0}, 404


class UserLogout(Resource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=str(current_user), fresh=False)
        refresh_token = create_refresh_token(current_user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": current_user,
        }, 200

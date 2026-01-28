from flask import Blueprint, request
from bson.objectid import ObjectId

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from models.user_model import UserModel

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

def get_user_model(db):
    return UserModel(db)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return {"error": "All fields required"}, 400

    user_model = get_user_model(auth_bp.db)

    if user_model.find_by_email(email):
        return {"error": "User already exists"}, 409

    user_model.create_user(name, email, password)
    return {"message": "User registered successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user_model = get_user_model(auth_bp.db)
    user = user_model.find_by_email(email)

    if not user:
        return {"error": "Invalid credentials"}, 401

    from flask_bcrypt import Bcrypt
    bcrypt = Bcrypt()

    if not bcrypt.check_password_hash(user["password_hash"], password):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=str(user["_id"]))
    return {"access_token": access_token}, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user_model = get_user_model(auth_bp.db)

    user = user_model.collection.find_one(
    {"_id": ObjectId(user_id)}
    )


    return {
        "name": user["name"],
        "email": user["email"]
    }, 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return {"message": "Logged out (mock)"}, 200

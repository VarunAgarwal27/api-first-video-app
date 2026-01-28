from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserModel:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, name, email, password):
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        user = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_at": datetime.utcnow()
        }

        self.collection.insert_one(user)
        return user

    def find_by_email(self, email):
        return self.collection.find_one({"email": email})

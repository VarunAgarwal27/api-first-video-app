from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os
from routes.auth_routes import auth_bp


load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["api_first_video_app"]

auth_bp.db = db
app.register_blueprint(auth_bp)


@app.route("/")
def health_check():
    return {"status": "API running"}, 200


if __name__ == "__main__":
    app.run(debug=True)



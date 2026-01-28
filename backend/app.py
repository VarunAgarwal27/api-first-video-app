from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["api_first_video_app"]


@app.route("/")
def health_check():
    return {"status": "API running"}, 200

if __name__ == "__main__":
    app.run(debug=True)

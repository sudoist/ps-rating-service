from flask import Flask
from flask_pymongo import PyMongo
import os

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI + MONGO_DB
mongo = PyMongo(app)

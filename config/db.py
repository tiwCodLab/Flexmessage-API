import os
from pymongo import MongoClient

mongodb_uri = "mongodb+srv://admin:1234@cluster0.k3ldto4.mongodb.net/"
db_connection = MongoClient(mongodb_uri)
db = db_connection["flexaverDB"]
collection = db["flexaverDB"]

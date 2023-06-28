from pymongo import MongoClient
import setting as ENV

db_connection = MongoClient(ENV.MONGODB_URI)
db = db_connection[ENV.DATABASE_NAME]
collection = db[ENV.DATABASE_NAME]

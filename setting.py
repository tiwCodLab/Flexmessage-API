from os import getenv
from dotenv import load_dotenv

load_dotenv('.env')

MONGODB_URI = str(getenv("MONGODB_URI"))
DATABASE_NAME = str(getenv("DATABASE_NAME"))

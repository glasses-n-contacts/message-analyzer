from pymongo import MongoClient
from variables import *


def get_db():
    client = MongoClient(MONGODB_URI)
    db = client[CLIENT_MONGODB]

    return db

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:1234@cluster0.4ahsat4.mongodb.net/"

client = MongoClient(uri, server_api=ServerApi('1'))


def get_db():
    try:
        client.server_info()
        print("Database is connected successfully.")
        return client.get_database("voicense_db")
    except Exception as e:
        print("Could not connect to the database. Error:", e)

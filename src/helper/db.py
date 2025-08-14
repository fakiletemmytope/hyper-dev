from pymongo import MongoClient
from pymongo.server_api import ServerApi
from src.config import db


uri = db


def get_client():
    client = MongoClient(
        uri,
        server_api=ServerApi(
            version="1",
            strict=True,
            deprecation_errors=True,
        ),
    )
    return client

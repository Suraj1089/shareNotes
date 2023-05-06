
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_DATABASE_URI


class DataBase:
    def __init__(self) -> None:
        self.client = MongoClient(MONGO_DATABASE_URI)

    async def close(self):
        self.client.close()

    def authenticate(self,username: str, password: str):
        self.client.db[]

    
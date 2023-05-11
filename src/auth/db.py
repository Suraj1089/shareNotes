
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_DATABASE_URI
from models import UserInDB
from hashing import Hash


class DataBase:
    def __init__(self) -> None:
        self.client = MongoClient(MONGO_DATABASE_URI)

    async def close(self):
        self.client.close()

    async def authenticate(self,username: str, password: str):
        return await self.client.sharenotes.auth.find_one({"username":username,"password":password})
    
    async def get_user(self,username: str):
        user = await self.client.sharenotes.auth.find_one({'username': username})
        if user:
            return 200,user 
        else:
            return 404,"User Not Found"
    
    async def register(self, username: str, password):
        user = self.get_user(username=username)
        if user:
            return "User with username already exist"
        
        hashed_password: str = Hash.get_password_hash(plain_password=password)
        self.client.sharenotes.auth.insert_one({"username":username,"password":hashed_password})

        return "User Created Successfully"
    



    

    
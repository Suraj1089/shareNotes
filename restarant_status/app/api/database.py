
from databases import Database
database = Database('sqlite+aiosqlite:///example.db')


class DataBase():
    def __init__(self,database):
        self.database = database

    async def connect(self):
        await self.database.connect()
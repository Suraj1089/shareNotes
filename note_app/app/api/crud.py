from .schemas import NoteSchema
from .db import notes, database
from datetime import datetime as dt


async def create_notes(payload: NoteSchema):
    query = f"INSERT INTO notes VALUES (title={payload.title},dscription={payload.description},completed={payload.completed},created_date={payload.created_date})"
    return database.execute(query=query)


async def get(id: int):
    query = f"SELECT * FROM notes WHEHRE id = {id}"
    return await database.execute(query=query)



async def get_all():
    query = "SELECT * FROM notes"
    return await database.fetch_all(query=query)




async def put(id:int, payload=NoteSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = f"UPDATE TABLE notes SET title = {payload.title}, description = {payload.description}, completed = {payload.completed}, created_date = {payload.created_date} WHERE id = {id}"
    return await database.execute(query=query)

async def delete(id: int):
    query = f"DELETE FROM notes WHERE id = {id}"
    return await database.execute(query=query)
from fastapi import APIRouter,Path,HTTPException
from typing import List
from .schemas import NoteDB,NoteSchema
from . import crud
from datetime import datetime as dt

notes = APIRouter(
    prefix='/notes',
    tags=["Notes"]
)



@notes.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0),):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@notes.get("/", response_model=List[NoteDB])
async def read_all_notes():
    print(await crud.get_all())
    return await crud.get_all()

@notes.put("/{id}/", response_model=NoteDB)
async def update_note(payload:NoteSchema,id:int=Path(...,gt=0)): #Ensures the input is greater than 0
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note_id = await crud.put(id, payload)
    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
    }
    return response_object

#DELETE route
@notes.delete("/{id}/", response_model=NoteDB)
async def delete_note(id:int = Path(...,gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.delete(id)

    return note

@notes.post("/", response_model=NoteDB, status_code=201)
async def create(payload: NoteSchema):
    # note_id = await crud.create_notes(payload)
    # print("***************************** ",note_id)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    response_object = {
        "id": 1,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
        "created_date": created_date,
    }
    return response_object


# async def create_note(payload: NoteSchema)
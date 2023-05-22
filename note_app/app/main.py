from fastapi import FastAPI
from .api.db import metadata,engine,database
from starlette.middleware.cors import CORSMiddleware
from .api.notes import notes


metadata.create_all(engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start():
    await database.connect()

@app.on_event("shutdown")
async def stop():
    await database.disconnect()


#include routes
app.include_router(notes)


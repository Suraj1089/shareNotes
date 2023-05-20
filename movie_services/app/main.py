from fastapi import FastAPI,status,HTTPException
from typing import List
from .apis.movies import movies
from .apis.db import metadata,database,engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")



@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# include routes
app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])

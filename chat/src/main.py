from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.db import  models
from .db.database import engine
from .routers import blog, user, authentication

app = FastAPI(
    openapi_url="/blog/api/v1/auth/openapi.json",
    docs_url="/blog/api/v1/docs/",
    redoc_url="/blog/api/v1/redoc/"
)
models.Base.metadata.create_all(engine)


@app.get("/", include_in_schema=False)
def redict_to_docs():
    return RedirectResponse(url='/blog/api/v1/docs')

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

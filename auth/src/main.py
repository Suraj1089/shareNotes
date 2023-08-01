from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .api.db import models
from fastapi.middleware.cors import CORSMiddleware
from .api.db.database import engine
from .api.routes import authentication,profile

# bind the engine
models.Base.metadata.create_all(bind=engine)
app = FastAPI(
    openapi_url="/api/v1/auth/openapi.json",
    docs_url="/api/v1/docs/",
    redoc_url="/api/v1/redoc/"
)

# setup middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/',include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url='/api/v1/docs')

app.include_router(router=authentication.auth)
app.include_router(router=profile.profile)
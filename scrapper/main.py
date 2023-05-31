from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api import routes
from starlette.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "base_url":os.getenv('BASE_URL'),
                                                      "auth_url": os.getenv('AUTH_URL'),
                                                      "recommender_url": os.getenv('RECOMMENDER_URL'),

                                                     })



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)
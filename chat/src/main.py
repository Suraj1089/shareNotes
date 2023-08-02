
import uvicorn
from fastapi import FastAPI,WebSocket
from .utils.socket_ import socket_app
from fastapi.middleware.cors import CORSMiddleware


app: FastAPI = FastAPI(
    title="Chat API",
    description="API for chat application",
    version="1.0.0",
    docs_url="/",
)
app.mount("/", socket_app)  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

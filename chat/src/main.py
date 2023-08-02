
import uvicorn
from fastapi import FastAPI
from .utils.socket_ import socket_app


app: FastAPI = FastAPI()

# Here we mount socket app to main fastapi app
app.mount("/", socket_app)  

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run('main:app',host='localhost',port=8000,reload=True)
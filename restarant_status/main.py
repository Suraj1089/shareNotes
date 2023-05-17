from typing import List

import databases
import uvicorn
from fastapi import FastAPI

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "mysql://root:Suraj%40123@localhost/my_loop"

# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

app = FastAPI()

async def get_all_menu():
    await database.connect()
    query = """SELECT * FROM menu_hours"""
    return await database.fetch_all(query=query)

@app.get('/')
def home():
    return {"data":"home page"}

@app.get('/trigger_report')
async def report_trigger():
    data = await get_all_menu()
    print(data)
    return {"report":"triggered"}

@app.get('/get_report')
def get_report():
    return {"data":"get report"}










if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)
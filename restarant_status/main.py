from typing import List

import databases
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uuid 
import asyncio
# SQLAlchemy specific code, as with any other app
DATABASE_URL = "mysql://root:Suraj%40123@localhost/my_loop"

# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

app = FastAPI()

async def load_menu_hours():
    await database.connect()
    query = """SELECT * FROM menu_hours"""
    return await database.fetch_all(query=query)

async def load_store_status():
    await database.connect()
    query = """SELECT * FROM store_status"""
    return await database.fetch_all(query=query)


async def load_bq_result():
    await database.connect()
    query = """SELECT * FROM store_status"""
    return await database.fetch_all(query=query)




def generate_report_data():
    report_data = None 
    return report_data

def store_report_path(report_id: str, report_path: str):
    pass 

def get_report_path(report_id: str):
    pass


async def generate_report(report_id: str):
    # Load data from CSVs and create database tables
    bq_result = await load_bq_result()
    menu_hours = await load_menu_hours()
    store_status = await load_store_status()
    
    # Generate the report
    report = generate_report_data(bq_result, menu_hours, store_status)
    
    # Save the report as a CSV
    report_path = f"report_{report_id}.csv"
    report.to_csv(report_path, index=False)
    
    # Store the report path in the database or any other storage mechanism
    store_report_path(report_id, report_path)


@app.get('/')
def home():
    return {"data":"home page"}

@app.post("/trigger_report")
async def trigger_report():
    # Generate a random report_id
    report_id = str(uuid.uuid4())
    
    # Asynchronously generate the report
    asyncio.create_task(generate_report(report_id))
    
    return {"report_id": report_id}


@app.get("/get_report")
async def get_report(report_id: str):
    # Check if the report generation is complete
    report_path = get_report_path(report_id)
    
    if report_path is None:
        return {"status": "Running"}
    
    # Return the report CSV
    return FileResponse(report_path)












if __name__ == '__main__':
    uvicorn.run('main:app',host='0.0.0.0',port=8000,reload=True)
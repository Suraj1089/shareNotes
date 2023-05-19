from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import pytz
import uuid
import databases
import uvicorn


# SQLAlchemy specific code, as with any other app
DATABASE_URL = "mysql://root:Suraj%40123@localhost/my_loop"

# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

app = FastAPI()

async def load_menu_hours():
    await database.connect()
    query = """SELECT * FROM menu_hours"""
    return await database.fetch_all(query=query)



app = FastAPI()

# Define the data models
class StoreStatus(BaseModel):
    store_id: int
    timestamp_utc: str
    status: str

class StoreHours(BaseModel):
    store_id: int
    day_of_week: int
    start_time_local: str
    end_time_local: str

class StoreTimezone(BaseModel):
    store_id: int
    timezone_str: str

class Report(BaseModel):
    store_id: int
    uptime_last_hour: int
    uptime_last_day: int
    uptime_last_week: int
    downtime_last_hour: int
    downtime_last_day: int
    downtime_last_week: int

# Database to store the CSV data (can be replaced with an actual database)
store_status_data = []
store_hours_data = []
store_timezone_data = []
report_data = {}

# Import the CSV data into the database
def import_csv_data():
    store_status_df = pd.read_csv("store_status.csv")
    store_hours_df = pd.read_csv("store_hours.csv")
    store_timezone_df = pd.read_csv("store_timezone.csv")

    global store_status_data, store_hours_data, store_timezone_data
    store_status_data = store_status_df.to_dict(orient="records")
    store_hours_data = store_hours_df.to_dict(orient="records")
    store_timezone_data = store_timezone_df.to_dict(orient="records")

# Function to calculate the uptime within business hours
def calculate_uptime(store_id: int, start_time: datetime, end_time: datetime) -> int:
    # Retrieve the store's status data
    status_data = [status for status in store_status_data if status['store_id'] == store_id]

    # Filter the status data within the provided time range
    filtered_data = [status for status in status_data if start_time <= status['timestamp_utc'] <= end_time]

    # Calculate the total uptime within business hours
    total_uptime = 0
    for i in range(len(filtered_data) - 1):
        current_status = filtered_data[i]['status']
        next_status = filtered_data[i+1]['status']
        if current_status == 'active' and next_status == 'active':
            uptime = filtered_data[i+1]['timestamp_utc'] - filtered_data[i]['timestamp_utc']
            total_uptime += uptime.total_seconds() // 60

    return int(total_uptime)

# Function to generate the report
def generate_report(store_id: int) -> Report:
    # Retrieve the store's business hours
    store_hours = [hours for hours in store_hours_data if hours['store_id'] == store_id]
    if not store_hours:
        return None

    # Retrieve the store's timezone
    store_timezone = next((timezone['timezone_str'] for timezone in store_timezone_data if timezone['store_id'] == store_id), 'America/Chicago')

    # Get the current UTC timestamp
    current_time_utc = datetime.now(pytz.utc)

    # Calculate the start and end time for the last hour, last day, and last week
    start_time_last_hour = current_time_utc - timedelta(hours=1)
    start_time_last_day = current_time_utc - timedelta(days=1)
    start_time_last_week = current_time_utc - timedelta(weeks=1)

    # Convert the start and end times to the store's local timezone
    timezone = pytz.timezone(store_timezone)
    start_time_last_hour_local = start_time_last_hour.astimezone(timezone)
    start_time_last_day_local = start_time_last_day.astimezone(timezone)
    start_time_last_week_local = start_time_last_week.astimezone(timezone)

    end_time_local = datetime.now(timezone)

    # Calculate the uptime for the last hour, last day, and last week
    uptime_last_hour = calculate_uptime(store_id, start_time_last_hour_local, end_time_local)
    uptime_last_day = calculate_uptime(store_id, start_time_last_day_local, end_time_local)
    uptime_last_week = calculate_uptime(store_id, start_time_last_week_local, end_time_local)

    # Placeholder values for downtime
    downtime_last_hour = 0
    downtime_last_day = 0
    downtime_last_week = 0

    # Create and return the report
    report = Report(
        store_id=store_id,
        uptime_last_hour=uptime_last_hour,
        uptime_last_day=uptime_last_day,
        uptime_last_week=uptime_last_week,
        downtime_last_hour=downtime_last_hour,
        downtime_last_day=downtime_last_day,
        downtime_last_week=downtime_last_week
    )
    return report

# Import CSV data on startup
import_csv_data()

# API endpoints
@app.post("/trigger_report", response_model=str)
def trigger_report():
    # Generate a unique report ID
    report_id = str(uuid.uuid4())

    # Start report generation in the background
    # Here, you can use a task queue or background job system like Celery to perform the report generation asynchronously

    # Store the report ID for later retrieval
    report_data[report_id] = None

    return report_id

@app.get("/get_report/{report_id}")
def get_report(report_id: str):
    # Check if the report generation is complete
    if report_id not in report_data:
        return "Invalid report ID"
    
    report = report_data[report_id]

    if report is None:
        return "Running"
    else:
        # Return the report as a CSV file
        report_csv = f"{report_id}.csv"
        report_df = pd.DataFrame([report.dict()])
        report_df.to_csv(report_csv, index=False)

        return FileResponse(report_csv, media_type="text/csv", filename=report_csv)


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

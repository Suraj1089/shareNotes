from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import pytz
import uuid
import psycopg2

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

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="store_monitoring",
    user="username",
    password="password"
)

# Function to import the CSV data into the database tables
def import_csv_data():
    # Import store_status.csv
    store_status_df = pd.read_csv("store_status.csv")
    store_status_df.to_sql("store_status", conn, if_exists="replace", index=False)

    # Import store_hours.csv
    store_hours_df = pd.read_csv("store_hours.csv")
    store_hours_df.to_sql("store_hours", conn, if_exists="replace", index=False)

    # Import store_timezone.csv
    store_timezone_df = pd.read_csv("store_timezone.csv")
    store_timezone_df.to_sql("store_timezone", conn, if_exists="replace", index=False)

# Function to calculate the uptime within business hours
def calculate_uptime(store_id: int, start_time: datetime, end_time: datetime) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        SELECT timestamp_utc
        FROM store_status
        WHERE store_id = %s AND status = 'active' AND timestamp_utc >= %s AND timestamp_utc <= %s
        ORDER BY timestamp_utc
        """,
        (store_id, start_time, end_time)
    )
    timestamps = [row[0] for row in cur.fetchall()]
    cur.close()

    total_uptime = 0
    for i in range(len(timestamps) - 1):
        uptime = (timestamps[i+1] - timestamps[i]).total_seconds() // 60
        total_uptime += uptime

    return int(total_uptime)

# Function to generate the report
def generate_report(store_id: int) -> Report:
    cur = conn.cursor()

    # Get the maximum timestamp from store_status table
    cur.execute("SELECT MAX(timestamp_utc) FROM store_status")
    max_timestamp = cur.fetchone()[0]

    # Get the store's business hours
    cur.execute(
        """
        SELECT day_of_week, start_time_local, end_time_local
        FROM store_hours
        WHERE store_id = %s
        """,
        (store_id,)
    )
    store_hours = cur.fetchall()

    # Get the store's timezone
    cur.execute(
        """
        SELECT timezone_str
        FROM store_timezone
        WHERE store_id = %s
        """,
        (store_id,)
    )
    timezone_str = cur.fetchone()[0]
    cur.close()

    # Calculate the start and end times for the last hour, last day, and last week
    start_time_last_hour = max_timestamp - timedelta(hours=1)
    start_time_last_day = max_timestamp - timedelta(days=1)
    start_time_last_week = max_timestamp - timedelta(weeks=1)

    # Convert start times to the store's local timezone
    timezone = pytz.timezone(timezone_str)
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

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import csv
import pandas as pd

app = FastAPI()


@app.get("/api/test")
async def root():
    return {"message": "Hello World"}


@app.get("/api/nb_activities_by_type")
async def nb_activities_by_type():
    activity_counts = {}

    with open("data/activities.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            activity_type = row["Activity Type"]
            activity_counts[activity_type] = activity_counts.get(activity_type, 0) + 1

    # Format data for Google Charts: [['Header1', 'Header2'], ['Row1', value1], ...]
    chart_data = [["Activity Type", "Number of Activities"]]
    for activity_type, count in activity_counts.items():
        chart_data.append([activity_type, count])

    return chart_data


@app.get("/api/nb_activities_by_type_panda")
async def nb_activities_by_type_panda():
    df = pd.read_csv("data/activities.csv")

    # Group by Activity Type and count
    activity_counts = df["Activity Type"].value_counts()

    # Format data for Google Charts: [['Header1', 'Header2'], ['Row1', value1], ...]
    chart_data = [["Activity Type", "Number of Activities"]]
    for activity_type, count in activity_counts.items():
        chart_data.append([activity_type, int(count)])

    return chart_data


@app.get("/api/nb_activities_by_date")
async def nb_activities_by_date():
    df = pd.read_csv("data/activities.csv")

    # Parse the Activity Date column and extract just the date
    df["Activity Date"] = pd.to_datetime(df["Activity Date"])
    df["Date"] = df["Activity Date"].dt.date

    # Count activities per date
    activity_counts = df["Date"].value_counts().sort_index()

    # Format data for Google Calendar Chart with arrayToDataTable format
    chart_data = [["Date", "Activities"]]
    for date, count in activity_counts.items():
        chart_data.append([date.isoformat(), int(count)])

    return chart_data

app.mount("/", StaticFiles(directory="front", html=True), name="static")
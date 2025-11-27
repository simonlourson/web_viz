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


@app.get("/api/speed_by_distance")
async def speed_by_distance():
    df = pd.read_csv("data/activities.csv")

    # Select relevant columns and convert to numeric
    df = df[["Distance", "Average Speed", "Activity Type"]]
    # Remove commas from numbers before converting to numeric
    df["Distance"] = df["Distance"].astype(str).str.replace(",", "")
    df["Distance"] = pd.to_numeric(df["Distance"], errors="coerce")
    df["Average Speed"] = pd.to_numeric(df["Average Speed"], errors="coerce")

    # Filter rows with valid Distance and Average Speed values
    df = df.dropna()
    df = df[(df["Distance"] > 0) & (df["Average Speed"] > 0)]

    # Remove Swim activities (outlier)
    df = df[df["Activity Type"] != "Swim"]

    # Get unique activity types
    activity_types = sorted(df["Activity Type"].unique())

    # Format data for Google Scatter Chart with separate columns per activity type
    # Each row represents one activity, with null for other activity types
    chart_data = [["Distance (m)"] + activity_types]
    for _, row in df.iterrows():
        distance = float(row["Distance"])
        speed = float(row["Average Speed"])
        activity_type = row["Activity Type"]

        # Create a row with the distance and speed only in the correct activity type column
        data_row = [distance]
        for atype in activity_types:
            data_row.append(speed if atype == activity_type else None)

        chart_data.append(data_row)

    return chart_data


@app.get("/api/numeric_columns")
async def numeric_columns():
    df = pd.read_csv("data/activities.csv")

    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    return numeric_cols


@app.get("/api/string_columns")
async def string_columns():
    df = pd.read_csv("data/activities.csv")

    # Select only string/object columns
    string_cols = df.select_dtypes(include=["object"]).columns.tolist()

    return string_cols


@app.get("/api/distinct_values_for_column")
async def distinct_values_for_column(column: str):
    df = pd.read_csv("data/activities.csv")

    # Get distinct values for the specified column
    distinct_values = df[column].unique().tolist()

    return distinct_values

# http://localhost:8000/api/numeric_values?axeX=Activity%20ID&axeY=Activity%20ID
@app.get("/api/numeric_values")
async def numeric_values(axeX: str, axeY: str, filterColumn: str = None, filterValue: str = None):
    print("debug numeric_values")
    print(axeX)
    print(axeY)
    df = pd.read_csv("data/activities.csv")

    # Apply filter if both filterColumn and filterValue are provided
    if filterColumn and filterValue:
        df = df[df[filterColumn] == filterValue]

    # Select only the two requested columns
    df_filtered = df[[axeX, axeY]]

    # Convert to list of lists for easy consumption
    data = df_filtered.values.tolist()

    return data

app.mount("/", StaticFiles(directory="front", html=True), name="static")
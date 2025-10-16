# Web Visualization Exercises

This repository contains Strava activity data (`data/activities.csv`) that you'll use to practice creating web visualizations.

## Getting Started

The `activities.csv` file contains sports activity data with the following key fields:
- **Activity Type**: Type of sport (Run, Ride, Swim, etc.)
- **Activity Date**: When the activity took place
- **Distance**: Distance covered (in km)
- **Average Speed**: Average speed during the activity (in m/s)
- **Elapsed Time**: Duration of the activity
- **Elevation Gain/Loss**: Elevation changes during the activity

## Exercises

### Exercise 1: Pie Chart - Activities by Type

**Goal**: Create a pie chart showing the distribution of activities by type.

**Requirements**:
- Parse the CSV data and count the number of activities for each type
- Create a pie chart using a visualization library (D3.js, Chart.js, or similar)
- Display percentages for each activity type
- Use different colors for each activity type
- Add a legend to identify each type

---

### Exercise 2: Calendar Chart - Activity Dates

**Goal**: Create a calendar heatmap showing when activities occurred throughout the year.

**Requirements**:
- Parse the activity dates from the CSV
- Create a calendar chart (similar to GitHub's contribution graph)
- Use color intensity to show the number of activities per day
- Display month and day labels
- Add tooltips showing the exact count and date on hover

---

### Exercise 3: Line Chart - Distance by Date

**Goal**: Create a line chart showing the distance covered over time.

**Requirements**:
- Parse dates and distances from the CSV
- Plot distance on the y-axis and date on the x-axis
- Add gridlines for better readability
- Include axis labels with units (km for distance)
- Add hover tooltips showing exact values
- Consider adding a trend line or moving average (bonus)

---

### Exercise 4: Scatter Plot - Speed vs Distance

**Goal**: Create a scatter plot showing the relationship between average speed and distance.

**Requirements**:
- Extract average speed and distance for each activity
- Convert speed from m/s to km/h for better readability
- Plot distance on the x-axis and speed on the y-axis
- Use different colors or shapes for different activity types (bonus)
- Add axis labels with units
- Include tooltips showing activity details on hover
- Add a correlation line or regression line (bonus)

**Skills**: Scatter plots, correlation analysis, data transformation

---

## Bonus Challenges

1. **Filtering**: Add UI controls to filter data by date range or activity type
5. **Dashboard**: Combine all charts into a single interactive dashboard

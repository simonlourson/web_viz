# Web Visualization Tutorial

This repository is an educational project designed to teach students about web visualization and the fundamentals of building modern web applications with separate backend and frontend components.

## Table of Contents
- [Stack Overview](#stack-overview)
- [Backend vs Frontend](#backend-vs-frontend)
- [Current Implementation](#current-implementation)
- [Getting Started](#getting-started)

## Stack Overview

This project uses a simple but powerful stack:

### Backend
- **Python 3.x** - Programming language
- **FastAPI** - Modern, fast web framework for building APIs
- **CSV** - Data storage format
- **resourcecode** - External library for fetching time series data

### Frontend
- **HTML** - Structure and markup
- **JavaScript** - Client-side interactivity
- **Google Charts** - Visualization library

## Backend vs Frontend

Understanding the separation between backend and frontend is crucial in modern web development:

### What is a Backend?

The **backend** is the "server-side" of your application. It runs on a server (or your local machine during development) and is responsible for:

- **Data Management**: Storing, retrieving, and processing data
- **Business Logic**: Performing calculations and data transformations
- **API Endpoints**: Providing interfaces for the frontend to request data
- **Security**: Controlling access to data and resources

In this project, the backend is written in **Python** using **FastAPI** (`main.py`).

### What is a Frontend?

The **frontend** is the "client-side" of your application. It runs in the user's web browser and is responsible for:

- **User Interface**: What users see and interact with
- **Visualization**: Displaying data in charts, graphs, and other visual formats
- **User Interactions**: Responding to clicks, form inputs, and other user actions
- **API Consumption**: Requesting data from the backend and displaying it

In this project, the frontend is built with **HTML** and **JavaScript** (`front/index.html`).

### How They Communicate

The frontend and backend communicate through **HTTP requests**:

1. The user interacts with the frontend (e.g., selects a year)
2. JavaScript makes an HTTP request to a backend API endpoint (e.g., `/api/time_series?year=2010`)
3. The backend processes the request, fetches/processes data, and returns a response
4. JavaScript receives the response and updates the visualization

## Current Implementation

### Backend (`main.py`)

The FastAPI application provides two API endpoints:

#### 1. `/api/test_data` (GET)
- Reads and returns data from `data.csv`
- Converts numeric strings to integers
- Example data: daily activities and hours spent

#### 2. `/api/time_series` (GET)
- Accepts a `year` parameter (defaults to 2010)
- Fetches environmental data from a specific geographic location (near Brest, France)
- Retrieves weather parameters: wind (uwnd, vwnd), temperature (t02), precipitation (tp), and cloud cover (cge)
- Returns data formatted for Google Charts visualization
- Example: `/api/time_series?year=2015`

#### Static File Serving
- The backend also serves the frontend files from the `front/` directory
- This allows the entire application to run from a single server

### Frontend (`front/index.html`)

The frontend provides an interactive visualization interface:

#### Features
- **Year Selector**: Dropdown menu to choose years from 2010-2020
- **Interactive Chart**: Line chart displaying time series data
- **Refresh Button**: Manually reload data
- **Google Charts Integration**: Professional-looking, interactive visualizations

#### How It Works
1. On page load, the `drawChart()` function is called
2. JavaScript fetches data from `/api/time_series` with the selected year
3. Google Charts library renders the data as a line chart
4. When the year changes, the chart automatically updates

### Data Files

#### `data.csv`
Sample dataset with daily activities:
```
Task,Hours per Day
Work,11
Eat,2
Watch TV,2
Sleep,7
```

This demonstrates basic CSV data handling and could be used for simple pie or bar chart examples.

## Getting Started

### Prerequisites
- Python 3.x installed
- Required Python packages: `fastapi`, `resourcecode`

### Installation

1. Install dependencies:
```bash
pip install "fastapi[standard]" resourcecode
```

### Running the Application

1. Start the backend server:
```bash
fastapi dev main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. The frontend will load automatically and display the time series visualization

### Exploring the Code

**For Students:**

- Examine `main.py` to understand how API endpoints are created
- Look at `front/index.html` to see how JavaScript fetches data and creates visualizations
- Try modifying the year range in the dropdown
- Experiment with different Google Charts types (bar, pie, scatter, etc.)
- Create a new endpoint using the `data.csv` file

## Learning Objectives

By studying this project, students will learn:

1. **Client-Server Architecture**: How frontend and backend work together
2. **RESTful APIs**: How to design and consume API endpoints
3. **Asynchronous JavaScript**: Using `async/await` to fetch data
4. **Data Visualization**: Creating interactive charts from data
5. **HTTP Communication**: Understanding requests, responses, and query parameters
6. **Modern Python Web Development**: Using FastAPI for rapid API development

## Next Steps

Ideas for extending this project:

- Add error handling for failed API requests
- Create visualizations using the `data.csv` dataset
- Add more interactive controls (date range pickers, location selector)
- Implement data filtering on the backend
- Add multiple chart types (bar, scatter, area)
- Style the frontend with CSS
- Add data caching to improve performance

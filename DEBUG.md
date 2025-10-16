# Debugging Guide

When building web applications with separate backend and frontend components, things can go wrong in multiple places. This guide will help you systematically identify and fix issues.

## Table of Contents
- [General Debugging Approach](#general-debugging-approach)
- [Backend Debugging](#backend-debugging)
- [Frontend Debugging](#frontend-debugging)
- [Common Issues and Solutions](#common-issues-and-solutions)

## General Debugging Approach

When something goes wrong, follow these steps in order:

1. **Identify the symptom** - What exactly isn't working?
2. **Check the backend terminal** - Are there Python errors?
3. **Check the browser console** - Are there JavaScript errors?
4. **Test the API directly** - Does the backend work independently?
5. **Isolate the problem** - Is it backend, frontend, or communication between them?

## Backend Debugging

### Step 1: Check the Terminal

When you run `fastapi dev main.py`, the terminal shows important information:

**What to look for:**
- Server startup messages (should see "Application startup complete")
- Incoming HTTP requests (GET, POST, etc.)
- Python error messages and stack traces
- Port number (default: 8000)

**Example of healthy output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Example of an error:**
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/path/to/main.py", line 12, in get_data
    with open('data.csv', 'r') as file:
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```

### Step 2: Test API Endpoints Directly

Instead of testing through the frontend, test your API endpoints directly in the browser:

**Test the endpoints:**

1. Open your browser and go to: `http://localhost:8000/api/test_data`
   - You should see JSON data from `data.csv`
   - If you see HTML instead, there's a routing issue

2. Test with parameters: `http://localhost:8000/api/time_series?year=2015`
   - You should see JSON array with time series data
   - Try different years (2010-2020), or no year at all

**What should you see?**
- **Good response**: JSON formatted data (arrays, objects)
- **Bad response**: Error page, blank page, or HTML when expecting JSON

**Example of good JSON response:**
```json
[["date", "uwnd", "vwnd", "t02", "tp", "cge"],
 ["2015-01-01T01:00:00", 5.2, 3.1, 8.5, 0.0, 0.75],
 ...]
```

### Step 3: Check for Common Backend Errors

**Import Errors:**
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** Install missing packages: `pip install fastapi uvicorn resourcecode`

**File Not Found:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```
**Solution:** Ensure `data.csv` exists in the same directory as `main.py`

**Python Syntax Errors:**
```
SyntaxError: invalid syntax
```
**Solution:** Check the line number in the error message and fix the syntax error in `main.py`

### Step 4: Use FastAPI's Interactive Documentation

FastAPI provides automatic API documentation:

1. Go to: `http://localhost:8000/docs`
2. You'll see all available endpoints
3. Click "Try it out" to test endpoints interactively
4. View request/response formats

This is an excellent way to test if your backend is working correctly!

## Frontend Debugging

### Step 1: Open Browser Developer Tools

**How to open:**
- **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
- **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
- **Safari**: Enable Developer menu in Preferences, then press `Cmd+Option+I`

### Step 2: Check the Console Tab

The **Console** shows JavaScript errors, warnings, and custom log messages.

**What to look for:**

**Network Errors:**
```
GET http://localhost:8000/api/time_series?year=2015 net::ERR_CONNECTION_REFUSED
```
**Meaning:** Backend server isn't running
**Solution:** Start the backend with `uvicorn main:app --reload`

**404 Errors:**
```
GET http://localhost:8000/api/time_seriess?year=2015 404 (Not Found)
```
**Meaning:** Typo in the URL or endpoint doesn't exist
**Solution:** Check the URL in your JavaScript code

**JavaScript Syntax Errors:**
```
Uncaught SyntaxError: Unexpected token '}' in JSON at position 42
```
**Meaning:** The backend returned invalid JSON
**Solution:** Check the backend response format

**CORS Errors:**
```
Access to fetch at 'http://localhost:8000/api/...' has been blocked by CORS policy
```
**Meaning:** Cross-Origin Resource Sharing issue (unlikely in this setup, but possible)
**Solution:** Add CORS middleware to FastAPI if serving from different ports

### Step 3: Check the Network Tab

The **Network** tab shows all HTTP requests made by your page.

**How to use it:**

1. Open Developer Tools
2. Click on the "Network" tab
3. Refresh the page or trigger an action
4. Look for your API requests (e.g., `time_series?year=2015`)

**What to examine:**

**Request Details:**
- **Status Code**:
  - `200` = Success
  - `404` = Not Found
  - `500` = Server Error
- **Request URL**: Is it correct?
- **Response**: Click on the request to see the actual data returned

**Example workflow:**

1. Select a year from the dropdown
2. Watch the Network tab - you should see a request to `/api/time_series?year=XXXX`
3. Click on that request
4. Check the "Response" sub-tab to see the data returned
5. Check the "Headers" sub-tab to see request details

### Step 4: Use Console.log() for Debugging

Add `console.log()` statements to your JavaScript to understand what's happening:

**Example:**
```javascript
async function drawChart() {
  const year = document.getElementById('yearSelect').value;
  console.log('Selected year:', year);  // Debug: What year was selected?

  const response = await fetch(`/api/time_series?year=${year}`);
  console.log('Response status:', response.status);  // Debug: Did request succeed?

  const chartData = await response.json();
  console.log('Chart data:', chartData);  // Debug: What data did we receive?

  // ... rest of the code
}
```

Then check the browser console to see these messages!

### Step 5: Check for Common Frontend Errors

**Google Charts Not Loading:**
```
Uncaught ReferenceError: google is not defined
```
**Solution:** The Google Charts library hasn't loaded yet. Ensure the script tag is present and `google.charts.setOnLoadCallback()` is used.

**Element Not Found:**
```
Uncaught TypeError: Cannot read property 'value' of null
```
**Solution:** The HTML element doesn't exist. Check that `id` attributes match between HTML and JavaScript.

**Invalid Data Format:**
```
Error: Type mismatch. Value 2015-01-01T01:00:00 does not match type number
```
**Solution:** Google Charts expects specific data types. Check your backend data format matches chart requirements.

## Common Issues and Solutions

### Issue: "Page Shows HTML Instead of JSON When Testing API"

**Problem:** Going to `http://localhost:8000/api/test_data` shows the frontend HTML page instead of JSON.

**Possible Causes:**
1. The route is not correctly defined in `main.py`
2. The static files mount is overriding API routes

**Solution:**
- Ensure API routes are defined BEFORE `app.mount("/", ...)` in `main.py`
- API routes must start with `/api/` to avoid conflicts

### Issue: "Chart Doesn't Update When Year Changes"

**Debug Steps:**

1. **Check Browser Console** - Are there any JavaScript errors?
2. **Check Network Tab** - Is a new request made when you change the year?
3. **Add console.log()** - Log the selected year value
4. **Test API Directly** - Does the API work with different year parameters?

**Possible Solutions:**
- Ensure `onchange="onYearChange()"` is set on the `<select>` element
- Check that `onYearChange()` function calls `drawChart()`
- Verify the year parameter is correctly passed to the API

### Issue: "Nothing Happens When I Load the Page"

**Debug Steps:**

1. **Check if backend is running** - Look at terminal, should see "Application startup complete"
2. **Check browser console** - Are there JavaScript errors?
3. **Check Network tab** - Is the page making any requests?
4. **Test Google Charts** - Is the library loading? Check for `google is not defined` errors

**Possible Solutions:**
- Ensure server is running: `uvicorn main:app --reload`
- Check internet connection (needed for Google Charts CDN)
- Verify `google.charts.setOnLoadCallback(drawChart)` is called

### Issue: "Backend Returns 500 Internal Server Error"

**Debug Steps:**

1. **Check terminal immediately** - The full error will be there
2. **Read the stack trace** - Find the line number in your code
3. **Test with simple data** - Does the endpoint work with hardcoded data?

**Common Causes:**
- Missing file (`data.csv`, etc.)
- External API failure (`resourcecode` library issue)
- Data type mismatch
- Missing or incorrect function parameters

### Issue: "ModuleNotFoundError for 'resourcecode'"

**Problem:** Python can't find the `resourcecode` module.

**Solution:**
```bash
pip install resourcecode
```

If that doesn't work, check if you're using a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install packages
pip install fastapi uvicorn resourcecode
```

## Debugging Checklist

When something goes wrong, work through this checklist:

- [ ] Is the backend server running? (Check terminal)
- [ ] Are there errors in the terminal? (Read them carefully)
- [ ] Can I access the API directly in the browser?
- [ ] Are there errors in the browser console? (Press F12)
- [ ] Does the Network tab show the API request being made?
- [ ] What is the HTTP status code? (200 = good, 404 = not found, 500 = server error)
- [ ] Does the API return valid JSON when tested directly?
- [ ] Have I added `console.log()` statements to understand the flow?
- [ ] Are all files in the correct location?
- [ ] Are all dependencies installed?

## Pro Tips

1. **Always check both** the terminal (backend) and browser console (frontend)
2. **Test APIs directly** in the browser before testing through the frontend
3. **Use console.log()** liberally - it's your best friend
4. **Read error messages carefully** - they usually tell you exactly what's wrong
5. **Make small changes** and test frequently - don't write lots of code before testing
6. **Check the Network tab** to see exactly what data is being sent and received
7. **Use FastAPI docs** at `http://localhost:8000/docs` to test your API interactively

## Getting Help

If you're still stuck:

1. **Read the error message** - Search for it online (Stack Overflow, GitHub issues)
2. **Simplify** - Remove code until it works, then add back piece by piece
3. **Compare** - Look at working examples and compare with your code
4. **Ask for help** - Share the specific error message and what you've tried

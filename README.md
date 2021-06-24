# Quick-Weather-Checker
Simple Flask app using the openweathermap (https://openweathermap.org/api) api.

The app fetches weather information about the user-inputted city.

It fetches temperature, wind, rain of time periods, and also calculates the "best" period to go outside with an index combining the three values.

## Requirements
Python 3.8.5+

## How to use
1. Install dependencies
```
pip install -r requirements.txt
```
2. Run app.py

3. Go to http://localhost:5000 in your browser

4. Search for a city. The app will default to New York if the city is invalid.

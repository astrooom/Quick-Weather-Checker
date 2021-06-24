# Quick-Weather-Checker
Simple Flask app using the openweathermap api.
(https://openweathermap.org/api)

The app fetches weather information about city the user has input.

It fetches temperature, wind and rain of certain time periods each day in a 7-day period, and also calculates the "best" period to go outside with an index combining the three values, where high temperature, low rain and low wind gives a higher score.

## Requirements
Python 3.8.5+

## How to use
1. Install dependencies
```
pip install -r requirements.txt
```
2. Run app.py in VSCode or your favourite code editor

3. Go to http://localhost:5000 in your browser

4. Search for a city. The app will default to New York if the city is invalid.

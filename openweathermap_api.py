import requests
import datetime

api_key = '392192639ddf3f0c103e89c90ced46c6'  # Openweathermap API key


def get_weather_records(city_name):

    # -------------API Information and values------------------

    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric'

    #url = f'http://bulk.openweathermap.org/snapshot/hourly_14.json.gz?appid={api_key}'

    try:
        response = requests.get(url)
        # Gets latitude and longitude location of city to be used for get_daily_weather function below
        location = response.json()["city"]["coord"]
    except:
        print("Error while retrieving data from Openweathermap")

    # --------------Create list to easier get max value of different weather values------------------

    temp_list = []
    wind_list = []
    rain_list = []
    score_list = []

    # ---------------Iterate all the weather spells (3h periods for 5 days) and name values--------------------------

    try:  # Function will return None (null) if api can't find the city
        for spell in response.json()["list"]:

            spell_date_raw = spell["dt_txt"]

            spell_date_split = spell_date_raw.split(" ")

            # Formats date to 01-01-2020 at 09:00
            spell_date = f'{spell_date_split[0]} at {spell_date_split[1]}'

            spell_data = spell["main"]
            #spell_temp_feelslike = spell_data["feels_like"]

            #spell_weather = spell["weather"]

            #spell_visibility = spell["visibility"]

        # --------Rain values (not all weather periods have rain information - try/except. Has to be set to 0 to work with max() function)---------------
            try:
                spell_rain = spell["rain"]
                spell_rain_3h = spell_rain["3h"]
            except:
                spell_rain_3h = 0.00
            rain_list.append(spell_rain_3h)

        # --------Wind values----------------
            try:
                spell_wind = spell["wind"]
                spell_wind_speed = spell_wind["speed"]
                wind_list.append(spell_wind_speed)
            except:
                pass

        # --------Temperature values----------------
            try:
                spell_temp = spell_data["temp"]
                temp_list.append(spell_temp)
            except:
                pass

        # ----------Score values (combines temperature, wind and rain of period to calculate a score----------------
            spell_score = (spell_temp - spell_wind_speed - spell_rain_3h)
            score_list.append(spell_score)
            #print("date:", spell_date, "temp:", spell_temp, "wind:", spell_wind_speed, "rain:", spell_rain_3h, ":", "index:", spell_score)

        # --------Compare values of this iteration vs max value and set date if larger-----------------

            try:
                if spell_rain_3h >= max(rain_list):
                    highest_rain_spell = {
                        "date": spell_date, "wind": spell_wind_speed, "temperature": spell_temp, "rain": spell_rain_3h}
            except:
                pass

            try:
                if spell_wind_speed >= max(wind_list):
                    highest_wind_spell = {
                        "date": spell_date, "wind": spell_wind_speed, "temperature": spell_temp, "rain": spell_rain_3h}
            except:
                pass

            try:
                if spell_temp >= max(temp_list):
                    highest_temp_spell = {
                        "date": spell_date, "wind": spell_wind_speed, "temperature": spell_temp, "rain": spell_rain_3h}
            except:
                pass

            try:
                if spell_score >= max(score_list):
                    highest_score_spell = {"date": spell_date, "wind": spell_wind_speed,
                                           "temperature": spell_temp, "rain": spell_rain_3h, "score": spell_score}
            except:
                pass

        return {"rainiest": highest_rain_spell, "windiest": highest_wind_spell, "hottest": highest_temp_spell, "best": highest_score_spell, "location": location}
    except:
        return None

# print(get_weather_records("London"))


def get_daily_weather(city_location):

    daily_weather = []
# -------------API Information and values------------------
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={city_location["lat"]}&lon={city_location["lon"]}&exclude=current,minutely,hourly,alerts&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
    except:
        print("Error while retrieving data from Openweathermap")

    try:
        for day in response.json()["daily"]:

            day_weather_main = day["weather"][0]
            # Get short description of weather, example "Clouds, Rain, Clear etc to set an appropriate weather icon on page"
            day_weather_desc = day_weather_main["main"]

            day_date_timestamp = day["dt"]
            day_date_raw = datetime.datetime.fromtimestamp(
                int(day_date_timestamp)).strftime('%Y-%m-%d %H:%M:%S')
            day_date_split = day_date_raw.split(" ")
            # Formats date to 01-01-2020 at 09:00
            day_date = f'{day_date_split[0]} at {day_date_split[1]}'

            day_temp = day["temp"]["day"]
            day_wind_speed = day["wind_speed"]
            try:
                # Rain data not available of no rain recorded
                day_rain = day["rain"]["1h"]
            except:
                day_rain = 0.0

        # ---------Set weather icon based on how the weather is described from the API---------
            if day_weather_desc == "Clear":
                day_icon = 'icon-1.svg'
            elif day_weather_desc == "Clouds":
                day_icon = 'icon-6.svg'
            elif day_weather_desc == "Rain":
                day_icon = 'icon-9.svg'
            elif day_weather_desc == "Snow":
                day_icon = 'icon-13.svg'
            else:
                day_icon = 'icon-3.svg'

            daily_weather.append({"date": day_date, "description": day_weather_desc,
                                  "temperature": day_temp, "wind": day_wind_speed, "rain": day_rain, "icon": day_icon})

        return daily_weather
    except:
        return None


#daily_weather = get_daily_weather({'lat': 57.7072, 'lon': 11.9668})
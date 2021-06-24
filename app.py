from flask import Flask, render_template, request, redirect, flash, session
from openweathermap_api import get_weather_records, get_daily_weather


app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        city_name = request.form.get("searchcity")

        weather_records = get_weather_records(city_name)

        if weather_records:  # Checks if the city the user has searched for is valid, otherwise defaults to London and returns error
            rainiest = weather_records["rainiest"]
            windiest = weather_records["windiest"]
            hottest = weather_records["hottest"]
            best = weather_records["best"]

            # Uses latitude and longitude retrieved from the weather_records api call because https://openweathermap.org/api/one-call-api doesn't allow searching for cities
            daily_weather = get_daily_weather(weather_records["location"])

            return render_template("index.html",
                                   city_name=city_name,
                                   daily_weather=daily_weather,
                                   rainiest=rainiest,
                                   windiest=windiest,
                                   hottest=hottest,
                                   best=best)
        else:
            flash("Please enter a valid city.", "error")
            return redirect("/")

    else:  # Default Fallback
        city_name = "New York"
        weather_records = get_weather_records(city_name)
        rainiest = weather_records["rainiest"]
        windiest = weather_records["windiest"]
        hottest = weather_records["hottest"]
        best = weather_records["best"]
        daily_weather = get_daily_weather(weather_records["location"])
        return render_template("index.html",
                               city_name=city_name,
                               daily_weather=daily_weather,
                               rainiest=rainiest,
                               windiest=windiest,
                               hottest=hottest,
                               best=best)


if __name__ == "__main__":
    app.run(debug=True)

import datetime
import pytz
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = open("api_key.txt", "r").read()

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * 9 / 5 + 32
    return celsius, fahrenheit

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'London'

    url = f"{BASE_URL}?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        temp_kelvin = data["main"]["temp"]
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        temp_feels_like_kelvin = data["main"]["feels_like"]
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(temp_feels_like_kelvin)
        wind_speed = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"], tz=pytz.UTC)
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"], tz=pytz.UTC)
    else:
        error_message = data["message"]
        return render_template('error.html', error_message=error_message)

    return render_template('index.html', city=city, temp_celsius=temp_celsius, temp_fahrenheit=temp_fahrenheit,
                           feels_like_celsius=feels_like_celsius, feels_like_fahrenheit=feels_like_fahrenheit,
                           wind_speed=wind_speed, humidity=humidity, description=description,
                           sunrise_time=sunrise_time, sunset_time=sunset_time)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

my_api_key = 'M6Uk03MDYG6lOQ6zHr5gcj5skUcUjEpd'
location_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
weather_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/'
# Получаем location_key и данные о погоде
def get_location_key(latitude, longitude):
    try:
        response = requests.get(location_url, params={
            'apikey': my_api_key,
            'q': f'{latitude},{longitude}'
        })
        response.raise_for_status()
        data = response.json()
        return data.get('Key')
    except requests.RequestException:
        return None
def get_weather_data(location_key):
    try:
        response = requests.get(f"{weather_url}{location_key}", params={
            'apikey': my_api_key,
            'details': 'true'
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
def check_bad_weather(temperature, wind_speed, precipitation_chance):
    if temperature < 0 or temperature > 35:
        return True
    elif wind_speed > 50:
        return True
    elif precipitation_chance > 70:
        return True
    return False
# Реализация веб-интерфейса для оценки погодных условий при вводе широты и долготы
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        location_key = get_location_key(latitude, longitude)
        if location_key:
            weather_data = get_weather_data(location_key)
            if weather_data and 'DailyForecasts' in weather_data:
                try:
                    temperature = weather_data['DailyForecasts'][0]['Temperature']['Maximum']['Value']
                    wind_speed = weather_data['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']
                    precipitation_chance = weather_data['DailyForecasts'][0]['Day']['PrecipitationProbability']
                    weather_bad_results = check_bad_weather(temperature, wind_speed, precipitation_chance)
                    return render_template('result_weather.html', bad_weather=weather_bad_results)
                except (KeyError, TypeError):
                    return "Ошибка обработки данных."
            else:
                return "Погода не найдена"
        else:
            return "Место не найденo"
    return render_template('input_form.html')
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import requests
from functools import lru_cache
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Конфигурация
API_KEY = os.getenv('WEATHER_API_KEY', 'M6Uk03MDYG6lOQ6zHr5gcj5skUcUjEpd')
LOCATION_URL = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
WEATHER_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/'

# Кэширование запросов на 30 минут
@lru_cache(maxsize=100)
def get_location_key(latitude, longitude):
    try:
        response = requests.get(
            LOCATION_URL,
            params={
                'apikey': API_KEY,
                'q': f'{latitude},{longitude}'
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return data.get('Key')
    except requests.RequestException as e:
        app.logger.error(f"Error fetching location: {str(e)}")
        return None

@lru_cache(maxsize=100)
def get_weather_data(location_key):
    try:
        response = requests.get(
            f"{WEATHER_URL}{location_key}",
            params={
                'apikey': API_KEY,
                'details': 'true'
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        app.logger.error(f"Error fetching weather: {str(e)}")
        return None

def check_bad_weather(temperature, wind_speed, precipitation_chance):
    conditions = {
        'temperature': temperature < 0 or temperature > 35,
        'wind': wind_speed > 50,
        'precipitation': precipitation_chance > 70
    }
    return conditions

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            latitude = float(request.form.get('latitude'))
            longitude = float(request.form.get('longitude'))
            
            # Валидация координат
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                return render_template('error.html', message="Некорректные координаты")

            location_key = get_location_key(latitude, longitude)
            if not location_key:
                return render_template('error.html', message="Местоположение не найдено")

            weather_data = get_weather_data(location_key)
            if not weather_data or 'DailyForecasts' not in weather_data:
                return render_template('error.html', message="Данные о погоде недоступны")

            forecast = weather_data['DailyForecasts'][0]
            conditions = check_bad_weather(
                forecast['Temperature']['Maximum']['Value'],
                forecast['Day']['Wind']['Speed']['Value'],
                forecast['Day']['PrecipitationProbability']
            )

            return render_template(
                'result_weather.html',
                conditions=conditions,
                temperature=forecast['Temperature']['Maximum']['Value'],
                wind_speed=forecast['Day']['Wind']['Speed']['Value'],
                precipitation=forecast['Day']['PrecipitationProbability']
            )

        except ValueError:
            return render_template('error.html', message="Пожалуйста, введите корректные числовые значения")
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            return render_template('error.html', message="Произошла ошибка при обработке запроса")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
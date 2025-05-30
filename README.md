# 🌤️ Погодный Анализатор

Веб-приложение для анализа погодных условий по географическим координатам. Приложение использует API AccuWeather для получения актуальных данных о погоде и предоставляет удобный интерфейс для их анализа.

## ✨ Особенности

- 🔍 Поиск погоды по географическим координатам
- 📊 Анализ трех ключевых параметров:
  - Температура (опасные значения: < 0°C или > 35°C)
  - Скорость ветра (опасное значение: > 50 км/ч)
  - Вероятность осадков (опасное значение: > 70%)
- 🎨 Современный и отзывчивый интерфейс
- 📱 Адаптивный дизайн для всех устройств
- ⚡ Быстрая работа благодаря кэшированию запросов
- 🛡️ Надежная обработка ошибок

## 🚀 Установка и запуск

1. Клонируйте репозиторий:
```bash 
git clone https://github.com/Maksim-driller/first-project.git
cd first-project
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` и добавьте ваш API ключ AccuWeather:
```
WEATHER_API_KEY=ваш_ключ_api
```

4. Запустите приложение:
```bash
python weather_app.py
```

5. Откройте браузер и перейдите по адресу:
```
http://localhost:5000
```

## 🛠️ Технологии

- Python 3.x
- Flask
- AccuWeather API
- HTML5
- CSS3


## 📝 Примеры использования

1. Введите координаты интересующего вас места:
   - Широта: 55.7558 (Москва)
   - Долгота: 37.6173 (Москва)

2. Нажмите кнопку "Проверить погоду"

3. Получите подробный анализ погодных условий с визуальными индикаторами

## 🔒 Безопасность

- API ключ хранится в переменных окружения
- Валидация всех входных данных
- Защита от некорректных запросов
- Таймауты для внешних запросов

## 👥 Автор 

-  https://github.com/Maksim-driller 



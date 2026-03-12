# InfoBot 🤖

InfoBot is a simple Telegram bot written in Python.

The bot can show the current weather in a city and send random interesting facts.
This project was created as a learning project while studying Telegram bot development.

---

## Features

* 🌤 Get current weather by city name
* 📚 Receive random interesting facts
* ℹ️ Help menu
* Reply keyboard interface

---

## Technologies

* Python
* python-telegram-bot
* requests
* python-dotenv
* OpenWeather API
* Useless Facts API

---

## Environment Variables

Create a `.env` file in the project directory.

You need:

* **Telegram Bot Token** — create a bot using @BotFather in Telegram.
* **Weather API Key** — get it from https://openweathermap.org/api

Example `.env`:

```
TOKEN=your_telegram_bot_token
WEATHER_API_KEY=your_weather_api_key
```

---

## Installation

Create a virtual environment:

```
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run the Bot

```
python bot.py
```

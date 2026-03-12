# Chuck Norris Joke Bot 🤠

A simple Telegram bot that sends random Chuck Norris jokes.

This project was created as a learning project while studying asynchronous programming and Telegram bot development with Python.

The bot fetches jokes from a public API and allows the user to get new jokes using an inline button.

---

## Features

* `/start` command to greet the user
* `/joke` command to get a random joke
* Inline button to request the next joke
* Asynchronous API requests
* Basic error handling and logging

---

## Technologies

* Python
* python-telegram-bot
* aiohttp
* python-dotenv
* Chuck Norris Jokes API

---


## Environment Variables

Create a `.env` file in the project directory.

You need to add your Telegram bot token:

```
TOKEN=your_telegram_bot_token
```

You can create a bot and get a token using **@BotFather** in Telegram.

---

## Installation

Clone the repository or navigate to the project folder.

Create a virtual environment:

```
python -m venv .venv
```

Activate the virtual environment.

Linux / macOS:

```
source .venv/bin/activate
```

Windows:

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run the Bot

Start the bot with:

```
python bot.py
```

The bot will start polling Telegram for updates.

---

## API Used

This project uses the public **Chuck Norris Jokes API**:

https://api.chucknorris.io/

Example endpoint used:

```
https://api.chucknorris.io/jokes/random
```
# TaskReminderBot ⏰

A simple Telegram bot for creating and managing personal task reminders.

This project was created as a learning project while studying asynchronous programming and Telegram bot development with Python and aiogram.

The bot allows users to add tasks, set reminders, and manage their to-do list directly in Telegram.

---

## Features

* `/start` command to greet the user
* `/add` command to create a new task with a reminder
* `/list` command to show all tasks
* `/clear` command to delete all tasks
* Inline buttons to mark tasks as done or delete them
* Asynchronous reminders
* Rate limiting middleware to prevent spam
* SQLite database for persistent storage

---

## Technologies

* Python
* aiogram
* aiosqlite
* python-dotenv

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

## Database

This project uses SQLite for storing tasks. The database file `tasks.db` will be created automatically in the project directory.

---

## License

This project is for educational purposes.

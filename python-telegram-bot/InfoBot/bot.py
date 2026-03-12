import os
import logging
import requests

from telegram import (
    Update,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from api import get_weather
from dotenv import load_dotenv


# Configure logging for debugging and monitoring bot activity
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("Error: TOKEN not found in environment variables")


# Reply keyboard menu shown to the user
keyboard = [
    ["🌤 Weather"],
    ["📚 Fact"],
    ["ℹ️ Help"]
]

menu = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


def get_fact():
    """Return a random interesting fact from the public API."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"

    response = requests.get(url)
    data = response.json()

    return data["text"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command and show welcome message with menu."""
    text = (
        "Hi!\n\n"
        "I'm info bot.\n"
        "I can show weather and interesting facts."
    )

    await update.message.reply_text(text, reply_markup=menu)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    text = (
        "Functions:\n\n"
        "🌤 Weather - find out the weather\n"
        "📚 Fact - random fact"
    )

    await update.message.reply_text(text)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main message handler for processing user input.
    Handles menu buttons and weather city input.
    """
    text = update.message.text

    # User selected weather option
    if text == "🌤 Weather":
        await update.message.reply_text("Enter name of city:")
        context.user_data["await_city"] = True

    # Waiting for user to enter city name
    elif context.user_data.get("await_city"):
        city = text
        weather = get_weather(city)

        if weather:
            await update.message.reply_text(weather)
        else:
            await update.message.reply_text("City not found.")

        context.user_data["await_city"] = False

    # User requested random fact
    elif text == "📚 Fact":
        fact = get_fact()
        await update.message.reply_text(fact)

    # User opened help
    elif text == "ℹ️ Help":
        await help_command(update, context)

    # Unknown message
    else:
        await update.message.reply_text("I don't understand your message")


def main():
    """Initialize and start the Telegram bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
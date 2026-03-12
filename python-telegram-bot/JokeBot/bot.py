import os
import logging
import aiohttp

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
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


# Inline keyboard for requesting another joke
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("Next joke", callback_data="next_joke")]
])


async def get_joke() -> str:
    """Fetch a random Chuck Norris joke from the public API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.chucknorris.io/jokes/random") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("value", "Joke not found")

                return "API returned an error"

    except Exception:
        return "Failed to get joke"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command and greet the user."""
    username = update.effective_user.first_name

    await update.message.reply_text(
        f"Hello, {username}!\n"
        "I'm the one who can make you laugh.\n"
        "Try the /joke command."
    )


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random joke with an inline button to get another one."""
    joke = await get_joke()
    await update.message.reply_text(joke, reply_markup=keyboard)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button callbacks."""
    query = update.callback_query
    await query.answer()

    if query.data == "next_joke":
        joke = await get_joke()
        await query.edit_message_text(joke, reply_markup=keyboard)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify the user if possible."""
    logger.error("Error while processing update:", exc_info=context.error)

    if isinstance(update, Update) and update.message:
        try:
            await update.message.reply_text(
                "An error occurred. Please try again later."
            )
        except Exception as e:
            logger.error(f"Error notifying user: {e}")


def main():
    """Initialize and start the Telegram bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.add_error_handler(error_handler)

    logger.info("Bot is starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
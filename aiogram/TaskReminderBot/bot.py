import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import task_handlers
from middlewares.rate_limit import RateLimitMiddleware
from database.db import init_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file

load_dotenv()
TOKEN = os.getenv("TOKEN")  # Bot token from environment



# Main entry point for the bot (no docstring as requested)
async def main():

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    await init_db()

    dp.message.middleware(RateLimitMiddleware())

    dp.include_router(task_handlers.router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="add", description="Add new task"),
        BotCommand(command="list", description="Show tasks"),
        BotCommand(command="clear", description="Delete all tasks"),
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
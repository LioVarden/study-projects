import asyncio
from aiogram.types import Message


async def remind_later(message: Message, text: str, minutes: int):
    """Send a reminder message to the user after a specified number of minutes."""
    await asyncio.sleep(minutes * 60)

    await message.answer(f"⏰ Reminder!\n\n{text}")
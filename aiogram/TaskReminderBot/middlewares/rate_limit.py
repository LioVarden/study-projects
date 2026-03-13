import time
from aiogram import BaseMiddleware


class RateLimitMiddleware(BaseMiddleware):
    """Middleware to limit the rate of user messages."""
    def __init__(self, limit_seconds: float = 1.0):
        """Initialize the middleware with a time limit between messages."""
        self.limit_seconds = limit_seconds
        self.user_timestamps = {}

    async def __call__(self, handler, event, data):
        """Process incoming events and enforce rate limiting per user."""
        user_id = event.from_user.id
        current_time = time.time()
        last_time = self.user_timestamps.get(user_id, 0)

        if current_time - last_time < self.limit_seconds:
            await event.answer(f"Please wait. Messages allowed every {self.limit_seconds} seconds.")
            return

        self.user_timestamps[user_id] = current_time
        return await handler(event, data)
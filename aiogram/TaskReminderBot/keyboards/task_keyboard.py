from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def task_keyboard(task_id: int):
    """Create an inline keyboard for a task with Done and Delete buttons."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Done",
                    callback_data=f"done_{task_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 Delete",
                    callback_data=f"delete_{task_id}"
                )
            ]
        ]
    )

    return keyboard
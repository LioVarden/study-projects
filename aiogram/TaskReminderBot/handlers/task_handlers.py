import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.task_form import TaskForm
from database.db import (
    add_task,
    get_tasks,
    mark_done,
    delete_task,
    clear_tasks
)

from services.scheduler import remind_later
from keyboards.task_keyboard import task_keyboard

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    """Send a welcome message and show available commands."""
    text = (
        "👋 <b>Task Reminder Bot</b>\n\n"
        "/add — create task\n"
        "/list — show tasks\n"
        "/clear — delete all tasks"
    )

    await message.answer(text)


@router.message(Command("add"))
async def add(message: Message, state: FSMContext):
    """Start the process of adding a new task."""
    await state.clear()
    await message.answer("✏️ Send task text")
    await state.set_state(TaskForm.waiting_for_text)


@router.message(TaskForm.waiting_for_text)
async def task_text(message: Message, state: FSMContext):
    """Handle the input of the task text from the user."""
    await state.update_data(text=message.text)
    await message.answer("⏰ In how many minutes remind?")
    await state.set_state(TaskForm.waiting_for_time)


@router.message(TaskForm.waiting_for_time)
async def task_time(message: Message, state: FSMContext):
    """Handle the input of the reminder time and save the task."""
    if not message.text.isdigit():
        await message.answer("Send number of minutes")
        return

    minutes = int(message.text)
    data = await state.get_data()

    await add_task(message.from_user.id, data["text"], minutes)
    asyncio.create_task(remind_later(message, data["text"], minutes))

    await message.answer(f"✅ Task saved. Reminder in {minutes} minutes")
    await state.clear()


@router.message(Command("list"))
async def list_tasks(message: Message):
    """Show the list of tasks for the user."""
    tasks = await get_tasks(message.from_user.id)

    if not tasks:
        await message.answer("📭 No tasks")
        return

    await message.answer("<b>📋 Your tasks:</b>")

    for task in tasks:
        task_id = task[0]
        description = task[1]
        done = task[2]

        status = "✅" if done else "⬜"
        text = f"{task_id}. {description} {status}"

        if done:
            await message.answer(text)
        else:
            await message.answer(text, reply_markup=task_keyboard(task_id))


@router.callback_query(F.data.startswith("done_"))
async def done_callback(callback: CallbackQuery):
    """Mark a task as completed when the user clicks the 'Done' button."""
    task_id = int(callback.data.split("_")[1])

    tasks = await get_tasks(callback.from_user.id)

    for task in tasks:
        if task[0] == task_id and task[2] == 1:
            await callback.answer("Task already completed")
            return

    await mark_done(callback.from_user.id, task_id)

    await callback.answer("✅ Task completed")
    await callback.message.edit_text(callback.message.text + " ✅", reply_markup=None)


@router.callback_query(F.data.startswith("delete_"))
async def delete_callback(callback: CallbackQuery):
    """Delete a task when the user clicks the 'Delete' button."""
    task_id = int(callback.data.split("_")[1])
    await delete_task(callback.from_user.id, task_id)

    await callback.answer("🗑 Task deleted")
    await callback.message.delete()


@router.message(Command("clear"))
async def clear(message: Message):
    """Delete all tasks for the user."""
    await clear_tasks(message.from_user.id)
    await message.answer("🧹 All tasks deleted")
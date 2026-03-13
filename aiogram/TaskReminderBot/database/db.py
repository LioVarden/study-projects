import aiosqlite

DB_NAME = "tasks.db"  # Name of the SQLite database file


async def init_db():
    """Initialize the database and create the tasks table if it does not exist."""
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            description TEXT,
            remind_time INTEGER,
            done INTEGER DEFAULT 0
        )
        """)

        await db.commit()


async def add_task(user_id: int, text: str, remind_time: int):
    """Add a new task to the database for the given user."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO tasks(user_id, description, remind_time) VALUES(?,?,?)",
            (user_id, text, remind_time)
        )

        await db.commit()


async def get_tasks(user_id: int):
    """Retrieve all tasks for the given user."""
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id, description, done FROM tasks WHERE user_id=?",
            (user_id,)
        )

        return await cursor.fetchall()


async def mark_done(user_id: int, task_id: int):
    """Mark a specific task as done for the user."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE tasks SET done=1 WHERE id=? AND user_id=?",
            (task_id, user_id)
        )

        await db.commit()


async def delete_task(user_id: int, task_id: int):
    """Delete a specific task for the user."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "DELETE FROM tasks WHERE id=? AND user_id=?",
            (task_id, user_id)
        )

        await db.commit()


async def clear_tasks(user_id: int):
    """Delete all tasks for the given user."""
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            "DELETE FROM tasks WHERE user_id=?",
            (user_id,)
        )

        await db.commit()
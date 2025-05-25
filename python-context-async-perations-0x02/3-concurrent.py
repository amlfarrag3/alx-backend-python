import asyncio
import aiosqlite

# Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

# Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            return older_users

# Run both functions concurrently
async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    return results

asyncio.run(fetch_concurrently())

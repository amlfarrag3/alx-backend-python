
import aiosqlite
import asyncio

async def async_fetch_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users(db_path):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    db_path = "example.db"
    results = await asyncio.gather(
        async_fetch_users(db_path),
        async_fetch_older_users(db_path)
    )
    print("All users:", results[0])
    print("Users older than 40:", results[1])

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
  
